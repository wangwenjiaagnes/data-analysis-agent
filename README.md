# 账本数据分析 AI Agent

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，并填写你的配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入：
- `GROQ_API_KEY`: 你的 Groq API Key
- `SUPABASE_URL`: 你的 Supabase 项目 URL
- `SUPABASE_KEY`: 你的 Supabase API Key

### 3. 测试配置

```bash
python -m ledger_agent.config
```

### 4. 使用方式

#### 命令行测试

```bash
python -m ledger_agent.main "本月总支出是多少？"
```

#### 启动 API 服务

```bash
python -m ledger_agent.api
```

然后可以通过 HTTP 请求访问：

```bash
curl -X POST http://localhost:5001/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "本月总支出是多少？"}'
```

## 项目结构

```
ledger_agent/
├── __init__.py
├── config.py          # 配置管理
├── database.py        # 数据访问层
├── intent.py          # 意图识别层
├── analyzer.py        # 数据分析层
├── response.py        # 结果生成层
├── core.py            # 核心业务逻辑
├── main.py            # 命令行入口
└── api.py             # HTTP API 服务
```

## 部署

部署到 Railway/Render/Fly.io 时，确保：
1. 设置环境变量（GROQ_API_KEY, SUPABASE_URL, SUPABASE_KEY）
2. 启动命令：`python -m ledger_agent.api`

## 本地测试命令

以下命令可在项目根目录执行（需先 `source .venv/bin/activate`）：

| 目标 | 命令 |
|------|------|
| 验证配置 | `python -m ledger_agent.config` |
| 测试意图识别 | `python - <<'PY' ...`（调用 `IntentRecognizer` 的脚本） |
| 测试数据分析 | `python - <<'PY' ...`（调用 `Analyzer` 的脚本） |
| 测试回复生成 | `python - <<'PY' ...`（调用 `ResponseGenerator` 的脚本） |
| 完整流程（命令行） | `python -m ledger_agent.main "本月总支出是多少？"` |
| 启动 API | `python -m ledger_agent.api` |
| API 调用示例 | `curl -X POST http://localhost:5001/ask -H "Content-Type: application/json" -d '{"query": "..."}'` |

> 提示：也可以把这些命令整理为 `tests/` 或 `scripts/`，方便回归测试。

## 进阶部署

详细的 Railway/Render/Fly.io 部署说明见 `DEPLOYMENT.md`。

