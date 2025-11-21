"""
数据分析层
合并了数据访问、指标计算、工具执行
"""
from datetime import datetime, timedelta
from .database import Database


class Analyzer:
    """数据分析器"""
    
    def __init__(self):
        """初始化数据库连接"""
        self.db = Database()
    
    def get_date_range(self, date_range_type: str) -> tuple:
        """
        获取日期范围（使用 UTC 时区，确保服务器和本地一致）
        
        Args:
            date_range_type: "current_month" | "previous_month" | "last_7_days" | "last_30_days"
        
        Returns:
            (start_date, end_date) 格式为 YYYY-MM-DD
        """
        from datetime import timezone
        # 使用 UTC 时区，确保服务器和本地一致
        today = datetime.now(timezone.utc)
        
        if date_range_type == "current_month":
            start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = today
        elif date_range_type == "previous_month":
            # 上个月的第一天
            first_day_this_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            last_day_previous_month = first_day_this_month - timedelta(days=1)
            start_date = last_day_previous_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = last_day_previous_month.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif date_range_type == "last_7_days":
            end_date = today
            start_date = (today - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_range_type == "last_30_days":
            end_date = today
            start_date = (today - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            raise ValueError(f"Unknown date_range_type: {date_range_type}")
        
        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
    
    def compute_summary(self, transactions: list) -> dict:
        """
        计算汇总指标
        
        Args:
            transactions: 交易列表
        
        Returns:
            {
                "total_income": float,
                "total_expense": float,
                "net_balance": float,
                "transaction_count": int
            }
        """
        total_income = 0.0
        total_expense = 0.0
        
        for transaction in transactions:
            # 使用 cny_amount 字段（人民币金额），而不是 amount（原始金额，可能是多种货币）
            cny_amount = float(transaction.get("cny_amount", 0) or 0)
            transaction_type = transaction.get("type", "").lower()
            
            if transaction_type == "income":
                total_income += cny_amount
            elif transaction_type == "expense":
                total_expense += cny_amount
        
        net_balance = total_income - total_expense
        
        return {
            "total_income": round(total_income, 2),
            "total_expense": round(total_expense, 2),
            "net_balance": round(net_balance, 2),
            "transaction_count": len(transactions)
        }
    
    def analyze(self, params: dict) -> dict:
        """
        执行分析（合并了工具执行逻辑）
        
        Args:
            params: {
                "date_range": "current_month" | "previous_month" | "last_7_days" | "last_30_days"
            }
        
        Returns:
            {
                "intent": "summary",
                "total_income": float,
                "total_expense": float,
                "net_balance": float,
                "transaction_count": int,
                "date_range": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
            }
        """
        # 获取日期范围
        date_range_type = params.get("date_range", "current_month")
        transaction_type = params.get("type")
        
        # 标准化交易类型：将 "expenditure" 映射为 "expense"
        if transaction_type:
            transaction_type = transaction_type.lower()
            if transaction_type in ["expenditure", "expense", "支出"]:
                transaction_type = "expense"
            elif transaction_type in ["income", "收入"]:
                transaction_type = "income"

        start_date, end_date = self.get_date_range(date_range_type)
        
        # 查询数据
        transactions = self.db.query_transactions(start_date, end_date, transaction_type=transaction_type)
        
        # 计算指标
        result = self.compute_summary(transactions)
        
        return {
            "intent": "summary",
            **result,
            "date_range": {
                "start": start_date,
                "end": end_date
            }
        }

