# V1 实现计划（最小可行版本）

## 设计原则

1. **逐个功能跑通**：每个功能都要能独立验证（连接数据库、连接LLM、意图识别等）
2. **架构完整但简化**：保持7层架构，但每层先做最小实现
3. **接口先行**：定义清晰的接口，方便后续扩展
4. **可测试性**：每个模块都要能独立测试

---

## V1 功能范围

### 核心目标
**只实现一个完整的分析流程，验证整个架构可行**

### 选择：Summary（汇总概览）
- **为什么选 Summary**：
  - 功能相对简单，容易验证
  - 不涉及复杂的时间序列分析
  - 能验证数据库连接、LLM调用、结果生成等核心流程
  - 为后续功能打好基础

### V1 具体功能点

#### Summary 功能（简化版）
- ✅ 查询指定时间范围内的总支出
- ✅ 查询指定时间范围内的总收入
- ✅ 计算净收支（收入 - 支出）
- ✅ 支持时间参数：本月、上月、最近7天、最近30天

#### 不实现（V2再实现）
- ❌ 余额统计（需要账户余额表）
- ❌ 现金流统计（需要更复杂的逻辑）
- ❌ 分类汇总（先保证基础功能跑通）
- ❌ 其他意图（anomaly, trend, comparison 等）

---

## V1 架构设计（极简版 - 只保留核心层）

### V1 架构（3层核心架构）

```
第一层：意图识别层
  ├── 连接 Groq LLM API ✅
  ├── 识别单个意图（只识别 summary）✅
  └── 提取基础参数（时间范围）✅

第二层：数据分析层（合并了数据访问+指标计算+工具执行）
  ├── Supabase 连接 ✅
  ├── 日期处理函数 ✅
  ├── 数据查询 ✅
  └── 指标计算 ✅

第三层：结果生成层
  └── LLM 生成自然语言回复 ✅
```

### 为什么这样简化？

1. **结果聚合层**：V1 只有一个意图，不需要聚合 → 删除
2. **执行分析层**：V1 只有一个工具，不需要路由 → 合并到数据分析层
3. **指标定义层**：V1 指标简单，直接写在数据分析层 → 合并
4. **存储与通知层**：V2 再实现 → 删除

### 后续扩展路径

当需要添加新功能时，再逐步拆分：
- 添加多个意图时 → 拆分出执行分析层（工具路由）
- 添加多个指标时 → 拆分出指标定义层
- 添加多意图时 → 拆分出结果聚合层
- V2 时 → 添加存储与通知层

### 关键设计：接口先行

每个层都定义清晰的接口，即使实现简化，也要保证接口完整：

```python
# 示例：工具函数接口
def run_summary_analysis(params: dict) -> dict:
    """
    汇总分析工具
    
    Args:
        params: {
            "date_range": "current_month" | "previous_month" | "last_7_days" | "last_30_days",
            "start_date": "2024-01-01" (可选),
            "end_date": "2024-01-31" (可选)
        }
    
    Returns:
        {
            "intent": "summary",
            "total_income": 10000.00,
            "total_expense": 5000.00,
            "net_balance": 5000.00,
            "date_range": {...}
        }
    """
    pass
```

---

## V1 项目结构（极简版）

```
ledger_agent/
├── config.py              # 配置管理（API Key、数据库连接）
├── intent.py              # 意图识别层（LLM识别意图和参数）
├── analyzer.py            # 数据分析层（数据库查询 + 指标计算）
├── response.py            # 结果生成层（LLM生成回复）
├── core.py                # 核心业务逻辑（可被命令行和API共用）
├── main.py                # 命令行入口（用于测试）
├── api.py                 # HTTP API 服务（Flask/FastAPI）
├── test_*.py              # 各模块的测试文件
└── requirements.txt       # 依赖包
```

**说明**：
- `analyzer.py` 合并了原来的 `database.py` + `metrics.py` + `tools.py` + `executor.py`
- 后续扩展时，可以逐步拆分这些文件

---

## V1 开发步骤（逐个功能验证）

### 阶段1：基础环境搭建 ✅
1. **创建项目结构**
   - 创建所有文件（即使暂时为空）
   - 定义基础接口

2. **配置管理（config.py）**
   - 读取环境变量（Groq API Key、Supabase 连接信息）
   - 验证配置是否正确
   - **验证方式**：运行 `python -c "from config import *; print('Config loaded')"`

### 阶段2：数据访问验证 ✅
3. **Supabase 连接（analyzer.py）**
   - 连接 Supabase
   - 实现一个简单的测试查询（如：SELECT COUNT(*) FROM transactions）
   - **验证方式**：运行 `python test_analyzer.py`，确认能查询到数据

### 阶段3：LLM 连接验证 ✅
4. **Groq LLM 连接（intent.py 和 response.py）**
   - 测试 Groq API 调用
   - 实现一个简单的测试（如：让 LLM 返回 "Hello"）
   - **验证方式**：运行 `python test_llm.py`，确认能调用 LLM

### 阶段4：意图识别验证 ✅
5. **意图识别（intent.py）**
   - 实现识别 summary 意图
   - 提取时间参数（本月、上月等）
   - **验证方式**：运行 `python test_intent.py`，测试用例在代码中定义，确认能识别意图和参数

### 阶段5：数据分析验证 ✅
6. **数据分析（analyzer.py）**
   - 实现日期处理函数（get_date_range）
   - 实现数据查询（query_transactions）
   - 实现指标计算（compute_summary）
   - **验证方式**：运行 `python test_analyzer.py`，确认能正确计算指标

### 阶段6：结果生成验证 ✅
7. **结果生成（response.py）**
   - 实现 LLM 生成自然语言回复
   - **验证方式**：运行 `python test_response.py`，输入结果数据，确认能生成回复

### 阶段7：完整流程验证 ✅
8. **核心业务逻辑（core.py）**
   - 封装完整流程为可复用的类
   - **验证方式**：通过命令行和API都能调用

9. **命令行入口（main.py）**
   - 实现命令行版本（用于测试）
   - **验证方式**：运行 `python main.py "本月总支出是多少"`

10. **API 服务（api.py）**
    - 实现 HTTP API 接口
    - **验证方式**：运行 `python api.py`，然后发送 HTTP 请求测试

---

## V1 代码示例（关键接口）

### config.py
```python
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# 验证配置
def validate_config():
    assert GROQ_API_KEY, "GROQ_API_KEY not set"
    assert SUPABASE_URL, "SUPABASE_URL not set"
    assert SUPABASE_KEY, "SUPABASE_KEY not set"
```

### intent.py
```python
from groq import Groq
from config import GROQ_API_KEY

class IntentRecognizer:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
    
    def recognize(self, user_query: str) -> dict:
        """
        识别意图和参数
        
        Returns:
            {
                "intent": "summary",
                "params": {
                    "date_range": "current_month"
                }
            }
        """
        # 实现意图识别逻辑
        pass
```

### analyzer.py（合并了数据库+指标计算+工具执行）
```python
from supabase import create_client
from datetime import datetime, timedelta
from config import SUPABASE_URL, SUPABASE_KEY

class Analyzer:
    def __init__(self):
        self.client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    def get_date_range(self, date_range_type: str) -> tuple:
        """获取日期范围"""
        # 实现日期计算逻辑
        pass
    
    def query_transactions(self, start_date, end_date):
        """查询指定时间范围内的交易"""
        # 实现查询逻辑
        pass
    
    def compute_summary(self, transactions: list) -> dict:
        """计算汇总指标"""
        # 实现计算逻辑
        pass
    
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
                "date_range": {...}
            }
        """
        # 获取日期范围
        start_date, end_date = self.get_date_range(params["date_range"])
        
        # 查询数据
        transactions = self.query_transactions(start_date, end_date)
        
        # 计算指标
        result = self.compute_summary(transactions)
        
        return {
            "intent": "summary",
            **result,
            "date_range": {"start": start_date, "end": end_date}
        }
```

### response.py
```python
from groq import Groq
from config import GROQ_API_KEY

class ResponseGenerator:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
    
    def generate(self, result: dict, user_query: str) -> str:
        """生成自然语言回复"""
        # 实现 LLM 生成逻辑
        pass
```

### core.py（核心业务逻辑，可被命令行和API共用）
```python
from intent import IntentRecognizer
from analyzer import Analyzer
from response import ResponseGenerator

class AgentCore:
    def __init__(self):
        self.recognizer = IntentRecognizer()
        self.analyzer = Analyzer()
        self.generator = ResponseGenerator()
    
    def process_query(self, user_query: str) -> str:
        """处理用户问题，返回回复"""
        # 意图识别
        intent_result = self.recognizer.recognize(user_query)
        
        # 执行分析
        analysis_result = self.analyzer.analyze(intent_result["params"])
        
        # 生成回复
        response = self.generator.generate(analysis_result, user_query)
        
        return response
```

### main.py（命令行入口，用于测试）
```python
from core import AgentCore
import sys

def main():
    agent = AgentCore()
    
    # 用户输入方式1：命令行参数
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    # 用户输入方式2：交互式输入
    else:
        user_query = input("请输入您的问题: ")
    
    response = agent.process_query(user_query)
    print(response)

if __name__ == "__main__":
    main()
```

### api.py（HTTP API 服务）
```python
from flask import Flask, request, jsonify
from core import AgentCore

app = Flask(__name__)
agent = AgentCore()

@app.route('/ask', methods=['POST'])
def ask():
    """处理用户问题"""
    data = request.json
    user_query = data.get('query', '')
    
    if not user_query:
        return jsonify({'error': 'query is required'}), 400
    
    try:
        response = agent.process_query(user_query)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**使用方式**：
- **命令行测试**：运行 `python main.py "本月总支出是多少"`
- **API 服务**：运行 `python api.py`，然后通过 HTTP 请求访问
- **部署**：部署 `api.py` 到 Railway/Render/Fly.io

---

## V1 测试策略

每个模块都要有独立的测试文件：

- `test_config.py` - 测试配置加载
- `test_analyzer.py` - 测试数据库连接、查询和指标计算
- `test_llm.py` - 测试 LLM 连接
- `test_intent.py` - 测试意图识别（测试用例在代码中定义）
- `test_response.py` - 测试结果生成
- `test_main.py` - 测试完整流程

## V1 使用方式

### 开发测试
- 运行测试文件：`python test_*.py`
- 命令行测试：`python main.py "本月总支出是多少"`

### 本地 API 测试
```bash
# 启动 API 服务
python api.py

# 在另一个终端测试
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "本月总支出是多少"}'
```

### 部署上线
- 部署 `api.py` 到 Railway/Render/Fly.io
- 朋友可以通过 HTTP 请求访问：`POST https://your-app.railway.app/ask`

---

## V1 到 V2 的扩展路径

V1 完成后，扩展路径清晰：

1. **添加新意图**：
   - 在 `intent.py` 中添加识别逻辑
   - 在 `analyzer.py` 中添加新的分析方法（或拆分出 `tools.py`）

2. **拆分架构**（当代码变复杂时）：
   - 从 `analyzer.py` 拆分出 `database.py`（数据访问）
   - 从 `analyzer.py` 拆分出 `metrics.py`（指标计算）
   - 从 `analyzer.py` 拆分出 `tools.py`（工具函数）
   - 创建 `executor.py`（执行引擎，处理工具路由）

3. **多意图支持**：
   - 在 `executor.py` 中添加并行执行逻辑
   - 创建 `aggregator.py`（结果聚合层）

4. **链式执行**：
   - 在 `executor.py` 中添加链式触发逻辑

**关键**：V1 的接口设计要支持这些扩展，即使实现简化。当代码变复杂时再拆分，不要过早优化。

---

## V1 成功标准

✅ 能够连接 Supabase 并查询数据  
✅ 能够连接 Groq LLM 并调用 API  
✅ 能够识别 "本月总支出是多少" 这类问题  
✅ 能够计算并返回正确的汇总数据  
✅ 能够生成自然语言回复  
✅ 完整流程能够跑通（命令行版本）  
✅ API 服务能够正常响应 HTTP 请求  
✅ 可以部署到 Railway/Render/Fly.io 并远程访问  

---

## 下一步

完成 V1 后，再逐步添加：
- V1.1: 添加分类汇总功能
- V1.2: 添加 anomaly 意图
- V1.3: 添加 trend 意图
- V1.4: 添加 comparison 意图
- V2: 添加 attribution, forecast, optimization

