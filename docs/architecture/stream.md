# 流式输出系统

## 模块职责

流式输出模块（`EvoScientist/stream/`）处理 Agent 执行过程中的实时事件流，将其渲染到 CLI/TUI 或通道。

## 核心组件

| 文件 | 职责 |
|------|------|
| `emitter.py` | StreamEventEmitter — 标准化事件创建 |
| `tracker.py` | ToolCallTracker — 增量 JSON 解析工具参数 |
| `formatter.py` | ToolResultFormatter — 内容感知的结果格式化（Rich） |
| `state.py` | StreamState / SubAgentState — 流状态追踪、todo 解析 |
| `events.py` | `stream_agent_events()` — 异步事件生成器 |
| `display.py` | Rich 渲染函数（流式显示和最终输出） |
| `diff_format.py` | 文件编辑差异格式化 |
| `utils.py` | 工具函数和常量（截断、状态符号、行数统计） |

## 事件流

1. Agent 通过 LangGraph stream 产生事件
2. `stream_agent_events()` 将 LangGraph 事件转为 `StreamEvent`
3. `StreamEventEmitter` 创建标准化事件
4. `ToolCallTracker` 增量解析工具调用的 JSON 参数
5. `ToolResultFormatter` 格式化工具输出
6. `StreamState` 追踪当前状态（工具选择、子 Agent 等）
7. `display.py` 的 `create_streaming_display()` 渲染到终端

## 关键设计

- 工具选择器激活时（`_selector_active=True`），流式输出被抑制
- 编辑操作显示 diff 格式（`build_edit_diff` / `format_diff_rich`）
- 输出自动截断避免终端溢出
- Todo 列表实时解析和状态更新

## 模块间交互

- **← middleware/tool_selector.py**: 读取 `_selector_active` 和 `_current_selected_tools` 状态
- **→ cli/tui_runtime.py**: TUI 消费流式事件
- **→ channels/**: 通道通过 `send_thinking_message` 转发思考过程
