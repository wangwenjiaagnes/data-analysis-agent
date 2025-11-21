"""
HTTP API 服务
用于部署上线
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from .core import AgentCore
from .config import API_HOST, API_PORT

app = Flask(__name__)
CORS(app)  # 允许跨域请求
agent = AgentCore()


@app.route('/ask', methods=['POST'])
def ask():
    """处理用户问题"""
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        user_query = data.get('query', '')
        
        if not user_query:
            return jsonify({'error': 'query is required'}), 400
        
        response = agent.process_query(user_query)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'service': 'ledger_agent'
    })


@app.route('/debug/current-month', methods=['GET'])
def debug_current_month():
    """调试端点：查看本月查询情况"""
    try:
        from .analyzer import Analyzer
        analyzer = Analyzer()
        result = analyzer.analyze({"date_range": "current_month"})
        return jsonify({
            'status': 'success',
            'result': result
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, debug=True)

