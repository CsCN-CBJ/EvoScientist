# 测试策略

## 框架和工具

- **测试框架**: pytest（8.0+）
- **覆盖率**: pytest-cov（5.0+）
- **超时**: pytest-timeout（2.4+）
- **Lint**: Ruff（0.5+）
- **不需要 API Key**: 所有测试使用 mock

## 运行命令

```bash
uv run pytest                    # 运行全部测试
uv run pytest tests/test_config.py  # 运行单个文件
uv run pytest -k "test_mcp"     # 按名称过滤
uv run pytest --cov=EvoScientist   # 覆盖率
uv run ruff check .              # Lint
```

## 测试文件组织

测试位于 `tests/` 目录，按功能模块划分：

| 测试文件 | 覆盖模块 |
|----------|----------|
| test_backends.py | 沙盒后端、命令验证、路径修正 |
| test_config.py | 配置加载/保存/合并 |
| test_sessions.py | 会话持久化、线程管理 |
| test_llm.py | LLM 模型配置 |
| test_prompts.py | 提示词模板 |
| test_mcp_client.py | MCP 客户端 |
| test_agent_mcp_cache.py | MCP 工具缓存 |
| test_tools.py | 内置工具 |
| test_skills_manager.py | 技能管理器 |
| test_*_channel.py | 各消息通道 |
| test_channel_comprehensive.py | 通道通用功能 |
| test_bus_integration.py | MessageBus 集成 |
| test_*_middleware.py | 各中间件 |
| test_stream_*.py | 流式输出 |
| test_cli_*.py | CLI 功能 |
| test_tui_widgets.py | TUI 组件 |

## Mock 策略

- **LLM 调用**: Mock `init_chat_model` 和模型响应
- **外部 API**: Mock httpx 客户端和 SDK 调用
- **文件系统**: 使用 tmp_path fixture
- **MCP 服务器**: Mock 连接和工具发现
- **通道 SDK**: Mock 各平台 SDK 的消息收发

## 覆盖范围

- 核心模块（Agent 构建、配置、后端）覆盖率较高
- 各通道均有独立 smoke test
- 中间件有详细的单元测试
- CLI 命令有集成测试
