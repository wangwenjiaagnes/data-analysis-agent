"""
结果生成层
使用 LLM 将分析结果转换为自然语言回复
"""
from groq import Groq
from .config import GROQ_API_KEY, GROQ_MODEL


class ResponseGenerator:
    """回复生成器"""
    
    def __init__(self):
        """初始化 Groq 客户端"""
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not configured")
        
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL
    
    def generate(self, result: dict, user_query: str) -> str:
        """
        生成自然语言回复
        
        Args:
            result: 分析结果
            user_query: 原始用户问题
        
        Returns:
            自然语言回复
        """
        # 检测用户问题的语言（简单检测：如果包含中文字符，认为是中文）
        import re
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', user_query))
        response_language = "Chinese" if has_chinese else "English"
        
        # 格式化结果数据
        if has_chinese:
            result_text = f"""
分析结果：
- 总收入：{result.get('total_income', 0):.2f} 元
- 总支出：{result.get('total_expense', 0):.2f} 元
- 净收支：{result.get('net_balance', 0):.2f} 元
- 交易数量：{result.get('transaction_count', 0)} 笔
- 时间范围：{result.get('date_range', {}).get('start', '')} 至 {result.get('date_range', {}).get('end', '')}
"""
            system_prompt = "You are a professional ledger data analysis assistant. Respond in natural, friendly Chinese."
            user_prompt = f"""用户的问题是："{user_query}"

{result_text}

请用自然、友好的中文回复用户的问题。回复要：
1. 直接回答用户的问题
2. 包含关键数据（包括比例、净收支等）
3. 语言简洁明了
4. 不要重复说"根据分析结果"这类话

直接开始回复，不要其他说明：
"""
        else:
            # 计算比例（如果有收入）
            expense_ratio = None
            if result.get('total_income', 0) > 0:
                expense_ratio = (result.get('total_expense', 0) / result.get('total_income', 0)) * 100
            
            result_text = f"""
Analysis Results:
- Total Income: {result.get('total_income', 0):.2f} yuan
- Total Expense: {result.get('total_expense', 0):.2f} yuan
- Net Balance: {result.get('net_balance', 0):.2f} yuan
- Transaction Count: {result.get('transaction_count', 0)} transactions
- Date Range: {result.get('date_range', {}).get('start', '')} to {result.get('date_range', {}).get('end', '')}
"""
            if expense_ratio is not None:
                result_text += f"- Expense Ratio: {expense_ratio:.2f}% of total income\n"
            
            system_prompt = "You are a professional ledger data analysis assistant. Respond in natural, friendly English."
            user_prompt = f"""The user's question is: "{user_query}"

{result_text}

Please respond to the user's question in natural, friendly English. Your response should:
1. Directly answer the user's question
2. Include key data (including ratios, net balance, etc.)
3. Be concise and clear
4. Don't repeat phrases like "based on the analysis results"

Start your response directly, without any additional explanation:
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise Exception(f"Response generation failed: {str(e)}")

