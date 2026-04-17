# CLI / TUI 界面

## 模块职责

CLI 模块（`EvoScientist/cli/`）提供命令行和终端用户界面，是用户与 EvoScientist 交互的主要入口。

## 核心组件

| 模块 | 职责 |
|------|------|
| `__init__.py` | 入口函数 `main()`，Typer 应用定义 |
| `_app.py` | Typer 应用配置和子命令注册 |
| `agent.py` | Agent 会话管理（创建、恢复、新建） |
| `interactive.py` | 经典 CLI 交互模式 |
| `tui_interactive.py` | Textual TUI 交互模式 |
| `tui_runtime.py` | TUI 运行时环境 |
| `tui_backends.py` | TUI 后端抽象 |
| `commands.py` | 会话内斜杠命令（/new、/resume、/mcp 等） |
| `channel.py` | 通道管理 CLI 子命令 |
| `clipboard.py` | 剪贴板操作 |
| `file_mentions.py` | 文件提及解析（@file.py 语法） |
| `history_suggester.py` | 命令历史建议 |
| `status_bar.py` | 状态栏显示 |
| `mcp_ui.py` | MCP 管理 UI |
| `mcp_install_cmd.py` | MCP 安装命令 |
| `skills_cmd.py` | 技能管理命令 |
| `widgets/` | TUI 组件库（22 个组件） |

## 两种界面模式

- **TUI**（默认）— 全屏 Textual 界面，支持 Markdown 渲染、代码高亮、状态栏
- **CLI** — 经典命令行模式，`--ui cli` 启用，原生终端复制可用

## 会话内命令

| 命令 | 说明 |
|------|------|
| `/current` | 显示当前会话信息 |
| `/threads` | 列出最近会话 |
| `/resume` | 恢复之前的会话 |
| `/new` | 开始新会话 |
| `/skills` | 列出已安装技能 |
| `/install-skill <src>` | 安装技能 |
| `/mcp` | 管理 MCP 服务器 |
| `/channel` | 配置消息通道 |
| `/exit` | 退出 |

## 模块间交互

- **→ EvoScientist.py**: `create_cli_agent()` 创建带 checkpointer 的 Agent
- **→ sessions.py**: 线程管理（列出、恢复、删除）
- **→ config/settings.py**: 配置读写
- **→ stream/**: 流式事件显示
- **→ channels/**: 通道配置和管理
