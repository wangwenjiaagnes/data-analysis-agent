# 部署指南

## 环境变量

在云平台（Railway/Render/Fly.io）中配置以下环境变量：

| 变量名 | 说明 |
|--------|------|
| `GROQ_API_KEY` | Groq LLM 的 API Key |
| `GROQ_MODEL` | 可选，默认 `llama-3.3-70b-versatile` |
| `SUPABASE_URL` | Supabase 项目 URL |
| `SUPABASE_KEY` | Supabase service role key |
| `API_HOST` | 可选，默认 `0.0.0.0` |
| `API_PORT` | 可选，默认 `5000`（可根据平台要求调整） |

## 启动命令

```
python -m ledger_agent.api
```

确保平台的服务端口与 `API_PORT` 一致（例如 Railway 默认使用 `PORT` 环境变量，可设置 `API_PORT=$PORT`）。

## Railway 部署步骤

1. 登录 [Railway](https://railway.app/)，创建新项目。
2. 选择 “Deploy from GitHub” 或 “Deploy from Repo”，连接本项目仓库。
3. 在 Variables 中添加前述环境变量。
4. 在 “Settings → Deployments → Start Command” 中设置为 `python -m ledger_agent.api`。
5. 部署完成后，使用 `curl https://<railway-app-url>/ask` 测试。

## Render 部署步骤

1. 登录 [Render](https://render.com/)，创建 Web Service。
2. 选择仓库，Build Command 可设为 `pip install -r requirements.txt`。
3. Start Command 填 `python -m ledger_agent.api`。
4. 在 Environment 中添加所需变量，可将 `PORT` 同步给 `API_PORT`：`API_PORT=$PORT`。
5. 部署完成后，通过 Render 提供的 URL 测试。

## Fly.io 部署步骤（示例）

1. 安装 flyctl，运行 `fly launch` 初始化。
2. 编辑 `fly.toml`，设置服务端口与环境变量（`[env]` 段）。
3. 在 `Dockerfile` 或构建脚本中安装依赖并启动 API：
   ```Dockerfile
   CMD ["python", "-m", "ledger_agent.api"]
   ```
4. 运行 `fly deploy`，部署完成后通过 `fly open` 访问。

## 测试页面部署（可选）

测试页面 `test-page.html` 可以通过以下方式部署：

### 方案 1：GitHub Pages（推荐，最简单）

1. 在 GitHub 仓库设置中，进入 "Pages"
2. 选择 Source 为 `main` 分支，文件夹选择 `/ (root)`
3. 保存后，GitHub 会提供一个 URL，例如：`https://wangwenjiaagnes.github.io/data-analysis-agent/test-page.html`
4. 访问该 URL 即可使用测试页面

### 方案 2：Render Static Site

1. 在 Render Dashboard 创建 "Static Site"
2. 连接同一个 GitHub 仓库
3. Build Command 留空或设为 `echo "No build needed"`
4. Publish Directory 设为 `/`（根目录）
5. 部署后访问 `https://<your-site>.onrender.com/test-page.html`

### 方案 3：Netlify

1. 在 Netlify 连接 GitHub 仓库
2. Build command 留空
3. Publish directory 设为 `/`
4. 部署后访问 `https://<your-site>.netlify.app/test-page.html`

**注意**：测试页面调用的是 Render 上的 API（`https://data-analysis-agent-vn7n.onrender.com/ask`），确保 API 服务正常运行。

## 日志与监控

- Railway/Render 均可在控制台查看实时日志，便于排查错误。
- 建议在未来版本中加入应用层日志（请求耗时、错误堆栈等）。

## 安全与成本注意事项

- 切勿在仓库中提交 `.env` 或 service role key。
- Supabase service role key 具有写权限，如需更细粒度控制，可在未来版本通过自建中间层 API。
- Groq 按调用计费，部署上线后应增加速率限制或鉴权。


