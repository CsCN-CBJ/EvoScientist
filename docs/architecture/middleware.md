# 中间件系统

## 模块职责

中间件模块（`EvoScientist/middleware/`）提供 Agent 请求/响应处理管道，按顺序对每次 LLM 调用进行增强处理。

## 中间件链顺序

```
AskUserMiddleware（最外层，可选）
  → ContextEditingMiddleware
    → ContextOverflowMapperMiddleware
      → ToolErrorHandlerMiddleware
        → ConditionalToolSelectorMiddleware
          → ToolSelectionTrackerMiddleware
            → EvoMemoryMiddleware（最内层）
```

## 各中间件说明

### AskUserMiddleware

Agent 主动向用户提问以获取澄清。仅在 `enable_ask_user=True` 且非 `auto_mode` 时启用。

### ContextEditingMiddleware

基于 `ClearToolUsesEdit`，当对话 token 数达到上下文窗口 50% 时，清除旧的工具调用记录，保留最近 5 条。`think_tool` 被排除在清除范围之外。

- 触发阈值：`compute_context_editing_trigger(model, fraction=0.50)`
- 早于 `SummarizationMiddleware`（约 85%）触发

### ContextOverflowMapperMiddleware

将 LangGraph 的上下文溢出错误映射为可读的用户提示，而非让 Agent 崩溃。

### ToolErrorHandlerMiddleware

拦截子 Agent 的工具错误，提供包含 traceback 和重试指导的错误消息，提升子 Agent 的自我恢复能力。

### ConditionalToolSelectorMiddleware

当工具数量超过阈值（默认 26）时，通过额外一次 LLM 调用选择相关工具子集，减少噪音。`think_tool` 和 `task` 始终包含。

- 内部使用 `LLMToolSelectorMiddleware`，带 `_selector_active` 标志供流式层抑制输出
- 选择器失败时优雅降级（使用全部工具）

### ToolSelectionTrackerMiddleware

捕获工具选择后实际传入模型的工具列表，供流式显示使用。

### EvoMemoryMiddleware

自动从对话中提取和持久化长期记忆：

1. **注入**（每次 LLM 调用）：读取 `/memories/MEMORY.md` 追加到系统提示词
2. **提取**（阈值触发）：对话超过一定消息数时，使用 LLM 提取结构化事实并合并到 MEMORY.md

## 模块间交互

- **← llm/context_window.py**: ContextEditing 获取上下文窗口大小
- **← llm/models.py**: ToolSelector 和 Memory 使用 Chat Model
- **→ stream/events.py**: ToolSelectionTracker 状态供流式层读取
