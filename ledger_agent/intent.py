"""
意图识别层
使用 LLM 识别用户问题的意图和参数
"""
from groq import Groq
from .config import GROQ_API_KEY, GROQ_MODEL


class IntentRecognizer:
    """意图识别器"""
    
    def __init__(self):
        """初始化 Groq 客户端"""
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not configured")
        
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL
    
    def recognize(self, user_query: str) -> dict:
        """
        识别用户问题的意图和参数
        
        Args:
            user_query: 用户问题
        
        Returns:
            {
                "intent": "summary",
                "params": {
                    "date_range": "current_month" | "previous_month" | "last_7_days" | "last_30_days"
                }
            }
        """
        prompt = f"""你是一个账本数据分析助手。用户的问题是："{user_query}"

请识别用户的意图和参数，只返回 JSON 格式，不要其他文字。

可用的意图类型：
- summary: 汇总概览（如：总支出、总收入、净收支）

可用的时间范围参数：
- current_month: 本月
- previous_month: 上月
- last_7_days: 最近7天
- last_30_days: 最近30天

如果用户没有明确指定时间，默认使用 current_month。

返回格式：
{{
    "intent": "summary",
    "params": {{
        "date_range": "current_month"
    }}
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的意图识别助手，只返回 JSON 格式。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            result = response.choices[0].message.content
            import json
            return json.loads(result)
        
        except Exception as e:
            raise Exception(f"Intent recognition failed: {str(e)}")

