# 配置说明

EvoScientist 的配置优先级（从高到低）：CLI 参数 > 环境变量 > 配置文件 > 默认值。

## 配置文件

路径：`~/.config/evoscientist/config.yaml`（或 `$XDG_CONFIG_HOME/evoscientist/config.yaml`）

管理命令：

```bash
EvoSci onboard                # 交互式配置向导
EvoSci config set <key> <val> # 设置单项
EvoSci config list            # 列出所有配置
EvoSci config get <key>       # 获取单项
```

## 核心配置项

### LLM Provider

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| `provider` | - | `anthropic` | LLM provider |
| `model` | - | `claude-sonnet-4-6` | 默认模型 |
| `anthropic_api_key` | `ANTHROPIC_API_KEY` | - | Anthropic API Key |
| `openai_api_key` | `OPENAI_API_KEY` | - | OpenAI API Key |
| `google_api_key` | `GOOGLE_API_KEY` | - | Google API Key |
| `nvidia_api_key` | `NVIDIA_API_KEY` | - | NVIDIA API Key |
| `minimax_api_key` | `MINIMAX_API_KEY` | - | MiniMax API Key |
| `tavily_api_key` | `TAVILY_API_KEY` | - | 网页搜索 API Key |
| `reasoning_effort` | `EVOSCIENTIST_REASONING_EFFORT` | `high` | 推理努力程度 |

### 工作空间

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| `default_mode` | `EVOSCIENTIST_DEFAULT_MODE` | `daemon` | 工作空间模式（daemon/run） |
| `default_workdir` | `EVOSCIENTIST_WORKSPACE_DIR` | 当前目录 | 默认工作目录 |

### UI

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| `ui_backend` | `EVOSCIENTIST_UI_BACKEND` | `tui` | 界面模式（tui/cli） |
| `show_thinking` | - | `true` | 显示思考过程 |
| `log_level` | `EVOSCIENTIST_LOG_LEVEL` | `warning` | 日志级别 |

### HITL（Human-in-the-Loop）

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `auto_approve` | `false` | 自动批准 shell 命令 |
| `auto_mode` | `false` | 无人值守模式（隐含 auto_approve） |
| `shell_allow_list` | - | 自动批准的命令前缀（逗号分隔） |
| `enable_ask_user` | `true` | 启用 Agent 主动提问 |

### 通道

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `channel_enabled` | - | 启用的通道（逗号分隔） |
| `require_mention` | `group` | @提及要求（always/group/off） |
| `dm_policy` | `allowlist` | DM 访问策略（open/allowlist/pairing） |

各通道特定配置项见 [architecture/channels.md](architecture/channels.md) 和 [channels/README.md](../../EvoScientist/channels/README.md)。

### STT（语音转文字）

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `stt_enabled` | `false` | 启用语音转文字 |
| `stt_language` | `auto` | 语言（auto/zh/en） |
| `stt_device` | `cpu` | 设备（cpu/cuda） |
| `stt_compute_type` | `int8` | 计算精度 |

## MCP 配置

路径：`~/.config/evoscientist/mcp.yaml`

详见 [architecture/mcp.md](architecture/mcp.md)。

## 路径配置

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `EVOSCIENTIST_WORKSPACE_DIR` | 当前目录 | 工作空间根目录 |
| `EVOSCIENTIST_RUNS_DIR` | `<workspace>/runs` | 运行目录 |
| `EVOSCIENTIST_SKILLS_DIR` | `<workspace>/skills` | 项目技能目录 |
| `EVOSCIENTIST_MEMORIES_DIR` | `~/.config/evoscientist/memories` | 记忆目录（全局） |
| `EVOSCIENTIST_MEDIA_DIR` | `<workspace>/media` | 媒体文件目录 |
