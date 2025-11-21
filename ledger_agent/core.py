"""
核心业务逻辑
可被命令行和API共用
"""
from .intent import IntentRecognizer
from .analyzer import Analyzer
from .response import ResponseGenerator


class AgentCore:
    """AI Agent 核心类"""
    
    def __init__(self):
        """初始化各个组件"""
        self.recognizer = IntentRecognizer()
        self.analyzer = Analyzer()
        self.generator = ResponseGenerator()
    
    def process_query(self, user_query: str) -> str:
        """
        处理用户问题，返回回复
        
        Args:
            user_query: 用户问题
        
        Returns:
            自然语言回复
        """
        # 意图识别
        intent_result = self.recognizer.recognize(user_query)
        
        # 执行分析
        analysis_result = self.analyzer.analyze(intent_result["params"])
        
        # 生成回复
        response = self.generator.generate(analysis_result, user_query)
        
        return response

