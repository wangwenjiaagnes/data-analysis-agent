"""
数据访问层
Supabase 连接和查询封装
"""
from supabase import create_client, Client
from .config import SUPABASE_URL, SUPABASE_KEY


class Database:
    """Supabase 数据库封装"""
    
    def __init__(self):
        """初始化 Supabase 客户端"""
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("Supabase credentials not configured")
        
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    def query_transactions(self, start_date: str, end_date: str, transaction_type: str | None = None):
        """
        查询指定时间范围内的交易
        
        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            transaction_type: 可选，"income" 或 "expense"
        
        Returns:
            交易列表
        """
        start_iso = f"{start_date}T00:00:00+00:00"
        end_iso = f"{end_date}T23:59:59.999999+00:00"

        try:
            query = self.client.table("transactions").select("*").gte(
                "transaction_date", start_iso
            ).lte("transaction_date", end_iso)

            if transaction_type:
                query = query.eq("type", transaction_type.lower())

            response = query.execute()
            
            return response.data
        except Exception as e:
            raise Exception(f"Failed to query transactions: {str(e)}")
    
    def test_connection(self):
        """测试数据库连接"""
        try:
            # 简单查询测试
            response = self.client.table("transactions").select("id").limit(1).execute()
            return True
        except Exception as e:
            raise Exception(f"Database connection failed: {str(e)}")

