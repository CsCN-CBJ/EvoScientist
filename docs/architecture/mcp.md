# MCP 集成

## 模块职责

MCP 模块（`EvoScientist/mcp/`）实现 Model Context Protocol 集成，让 EvoScientist 连接外部工具服务器。

详细使用指南见 [mcp/README.md](../../EvoScientist/mcp/README.md)。

## 核心组件

| 文件 | 职责 |
|------|------|
| `client.py` | MCP 配置加载、工具发现、连接管理 |
| `registry.py` | MCP 工具注册和路由 |

## 配置

配置文件路径：`~/.config/evoscientist/mcp.yaml`

### 支持的传输方式

| Transport | 配置字段 |
|-----------|----------|
| stdio | command, args, env |
| http | url, headers |
| streamable_http | url, headers |
| sse | url, headers |
| websocket | url |

### 工具路由

`expose_to` 字段控制工具注入到哪些 Agent：

| Agent | 角色 |
|-------|------|
| main | 主编排器（默认） |
| planner-agent | 实验规划 |
| research-agent | 文献搜索 |
| code-agent | 代码编写 |
| debug-agent | 调试 |
| data-analysis-agent | 数据分析 |
| writing-agent | 报告撰写 |

### 工具过滤

`tools` 字段支持 glob 通配符过滤：`read_*`、`*_exa`、`get_metadata` 等。

## 关键设计

- MCP 工具按配置签名缓存，避免每次新建会话时重连
- 连接失败的服务器被跳过（不阻塞启动）
- 环境变量插值：YAML 中 `${VAR}` 在运行时解析
