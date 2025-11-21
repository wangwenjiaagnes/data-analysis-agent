# 账本数据分析 AI Agent 项目规划

## 1. 核心设计理念

### 1.1 顶层意图体系（8个意图类型）

所有分析需求统一到 8 个顶层意图类型，做到 MECE（相互独立、完全穷尽）：

- **summary** - 汇总概览：现在整体怎么样
- **trend** - 趋势：最近是在涨、在跌，还是差不多
- **comparison** - 对比：A 和 B 比起来如何
- **anomaly** - 异常：有没有哪里不正常
- **segmentation** - 分群/分类：不同类型/人群有什么不一样
- **attribution** - 归因：为什么会这样、是谁造成的
- **forecast** - 预测：未来可能会怎样
- **optimization** - 优化：我应该怎么做更好

**重要原则：**
- 意图识别层只输出这 8 个顶层意图
- 其他功能（预算分析、季节性分析、Top 支出等）作为这 8 个顶层意图下的子模式/参数
- **V1 版本实现**：summary, anomaly, trend, comparison（可选 segmentation）
- **V2 版本实现**：attribution, forecast, optimization

### 1.2 子模式设计

子功能通过参数传递，不建立独立意图分支。例如：
- 预算分析 → `comparison` + `sub_mode: "budget_comparison"`
- 季节性分析 → `trend` + `sub_mode: "seasonality"`
- Top 支出 → `segmentation` + `sub_mode: "top_spending"`

## 2. V1 核心功能

### Summary（汇总概览）
- 总收支统计、余额统计、现金流统计
- 基础指标：平均值、最大值、最小值
- 分类汇总

### Anomaly（异常检测）
- 识别异常交易、异常金额、异常模式
- 异常严重程度评估
- 子模式：fraud_detection, duplicate_detection, data_quality

### Trend（趋势分析）
- 收入/支出趋势、趋势方向判断、趋势强度评估
- 子模式：seasonality, volatility, momentum

### Comparison（对比分析）
- 周期对比、分类对比、账户对比、同比分析
- 子模式：budget_comparison, benchmark

### Segmentation（可选）
- 分类占比、Top 支出、消费模式识别

## 3. 架构设计

### 3.1 七层架构

```
第一层：意图识别层
  └── 自然语言理解 → 识别顶层意图（8选1或多选）→ 提取参数

第二层：执行分析层
  └── 执行策略判断 → 工具路由 → 工具函数库（按顶层意图组织）

第三层：指标定义层（新增）
  └── 统一指标计算、日期处理、业务规则（汇率、时区等）

第四层：数据访问层
  └── Supabase 查询封装、查询优化、数据缓存

第五层：结果聚合层
  └── 结果合并、优先级处理、冲突处理

第六层：结果翻译层
  └── 结果格式化 → LLM 自然语言生成

第七层：存储与通知层（V2实现）
  └── Insights 存储、定时任务、通知系统
```

### 3.2 执行模式

- **单意图执行**：单个意图 → 直接执行对应工具
- **多意图并行**：多个意图 → 并行执行所有工具 → 合并结果
- **链式执行**：工具结果满足条件 → 自动触发下一个工具（V2实现）

### 3.3 数据流（V1单意图场景）

```
用户提问
  ↓
意图识别层（LLM）→ 顶层意图 + 参数
  ↓
执行分析层 → 工具路由 → 工具函数
  ↓
指标定义层 → 统一指标计算
  ↓
数据访问层 → Supabase 查询
  ↓
结果聚合层 → 结果合并
  ↓
结果翻译层（LLM）→ 自然语言回复
  ↓
返回用户
```

## 4. 技术栈

- **LLM API**：Groq（兼容 OpenAI SDK）
- **LLM 模型**：llama-3.1-70b-versatile
- **编程语言**：Python
- **数据库**：Supabase（PostgreSQL）
- **部署平台**：Railway/Render/Fly.io 等

## 5. 项目结构

```
ledger_agent/
├── config.py              # 配置管理
├── intent.py              # 意图识别层
├── executor.py            # 执行分析层
├── tools.py               # 工具函数库（按顶层意图组织）
├── metrics.py             # 指标定义层（新增）
├── database.py            # 数据访问层
├── aggregator.py          # 结果聚合层
├── response.py            # 结果翻译层
├── main.py                # 主流程入口
├── scheduler.py           # 定时任务（V2）
├── notification.py        # 通知系统（V2）
└── insights_storage.py    # Insights 存储（V2）
```

## 6. 设计原则

1. **统一指标定义**：所有工具函数调用 `metrics.py` 中的指标函数，不直接写 SQL
2. **业务规则统一**：汇率、时区等规则在指标定义层统一处理
3. **子模式扩展**：通过参数扩展功能，不建立独立意图分支
4. **可扩展性**：架构支持多意图并行、链式执行等扩展能力

## 7. 后续版本规划

### V2 功能
- Attribution（归因分析）
- Forecast（预测分析）
- Optimization（优化建议）
- 定时任务、通知系统、可视化

---

**说明**：文档中的字段名示例（如 `sub_mode`, `is_anomaly` 等）是设计规范的一部分，不会影响开发，实际实现时可灵活调整。

