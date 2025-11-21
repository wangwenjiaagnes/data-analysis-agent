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
        # 格式化结果数据
        result_text = f"""
分析结果：
- 总收入：{result.get('total_income', 0):.2f} 元
- 总支出：{result.get('total_expense', 0):.2f} 元
- 净收支：{result.get('net_balance', 0):.2f} 元
- 交易数量：{result.get('transaction_count', 0)} 笔
- 时间范围：{result.get('date_range', {}).get('start', '')} 至 {result.get('date_range', {}).get('end', '')}
"""
        
        prompt = f"""用户的问题是："{user_query}"

{result_text}

请用自然、友好的中文回复用户的问题。回复要：
1. 直接回答用户的问题
2. 包含关键数据
3. 语言简洁明了
4. 不要重复说"根据分析结果"这类话

直接开始回复，不要其他说明：
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的账本数据分析助手，用自然、友好的中文回复用户。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise Exception(f"Response generation failed: {str(e)}")

