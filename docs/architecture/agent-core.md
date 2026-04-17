# Agent 核心

## 模块职责

Agent 核心模块（`EvoScientist/EvoScientist.py`）负责构建和初始化 EvoScientist 的多 Agent 图。它是整个系统的入口点，协调子 Agent、中间件、后端和工具的组装。

## 关键设计

### 延迟初始化

所有重量级初始化（DeepAgents、后端、LLM、中间件）延迟到首次使用时执行。这确保了轻量级 CLI 命令（如 `EvoSci config list`、`EvoSci onboard`）不会触发昂贵的导入和连接。

- `_ensure_config()` — 延迟加载并缓存配置
- `_ensure_chat_model()` — 延迟创建并缓存 LLM 实例
- `_get_default_agent()` — 延迟构建默认 Agent（含 MCP）

### MCP 工具缓存

MCP 工具按配置签名缓存（`_MCP_TOOLS_CACHE_KEY`），避免每次 `/new` 时重新连接 MCP 服务器。只有当 `mcp.yaml` 配置变更时才重新加载。

### Agent 构建流程

1. **构建后端** — `CompositeBackend`（workspace + skills + memories 三条路由）
2. **构建中间件链** — AskUser → ContextEditing → Overflow → ErrorHandler → ToolSelector → Memory
3. **加载子 Agent** — 从 `subagent.yaml` 读取定义，注入工具和中间件
4. **加载 MCP 工具** — 连接 MCP 服务器，按 `expose_to` 路由到对应 Agent
5. **创建 Agent** — `create_deep_agent()` 构建 LangGraph 图

### 两种 Agent 构建方式

- **默认 Agent**（`_get_default_agent`）— 无 checkpointer，用于 langgraph dev / notebook
- **CLI Agent**（`create_cli_agent`）— 带 SQLite checkpointer，支持多轮对话和 HITL（shell 命令审批）

## 子 Agent 体系

6 个子 Agent 在 `subagent.yaml` 中声明式定义：

| 子 Agent | 职责 | 工具 | 技能 |
|----------|------|------|------|
| planner-agent | 创建/更新实验计划 | think_tool | /skills/ |
| research-agent | 文献搜索 | tavily_search + think_tool | /skills/ |
| code-agent | 实现代码 | think_tool | /skills/ |
| debug-agent | 调试修复 | think_tool | /skills/ |
| data-analysis-agent | 数据分析 | think_tool | /skills/ |
| writing-agent | 撰写报告 | think_tool | /skills/ |

每个子 Agent 自动注入 ContextEditing、ErrorHandler、Overflow 中间件。MCP 工具按 `expose_to` 配置路由到对应子 Agent。

## 模块间交互

- **→ prompts.py**: 获取系统提示词和 RESEARCHER_INSTRUCTIONS 引用
- **→ backends.py**: 构建 CompositeBackend（workspace + skills + memories）
- **→ middleware/**: 组装中间件链
- **→ mcp/client.py**: 加载 MCP 工具（带缓存）
- **→ llm/models.py**: 获取 Chat Model 实例
- **→ config/settings.py**: 获取有效配置
- **→ sessions.py**: 获取 checkpointer（仅 CLI 模式）
- **→ utils.py**: `load_subagents()` 从 YAML 加载子 Agent 定义
