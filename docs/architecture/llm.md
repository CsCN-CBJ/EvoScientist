# LLM 模型配置

## 模块职责

LLM 模块（`EvoScientist/llm/`）提供统一的多 Provider 模型接入接口，基于 LangChain 的 `init_chat_model`。

## 支持的 Provider

| Provider | 路由方式 | 说明 |
|----------|----------|------|
| anthropic | 原生 | Claude 系列，默认支持 extended thinking |
| openai | 原生 | GPT 系列，默认启用 reasoning |
| google-genai | 原生 | Gemini 系列，自动启用 include_thoughts |
| nvidia | 原生 | NIM 端点 |
| ollama | 原生 | 本地模型 |
| openrouter | 原生 | 多模型路由，自动启用 reasoning |
| minimax | Anthropic 路由 | Anthropic 兼容端点 |
| kimi-coding | Anthropic 路由 | Anthropic 兼容端点 |
| custom-anthropic | Anthropic 路由 | 自定义 Anthropic 兼容端点 |
| deepseek | OpenAI 路由 | OpenAI 兼容端点 |
| moonshot | OpenAI 路由 | OpenAI 兼容端点 |
| siliconflow | OpenAI 路由 | OpenAI 兼容端点 |
| zhipu / zhipu-code | OpenAI 路由 | OpenAI 兼容端点 |
| volcengine | OpenAI 路由 | 豆包模型 |
| dashscope | OpenAI 路由 | 通义千问 |
| custom-openai | OpenAI 路由 | 自定义 OpenAI 兼容端点 |

## 核心组件

| 文件 | 职责 |
|------|------|
| `models.py` | 模型注册表（短名→模型ID映射）、`get_chat_model()` 工厂函数、provider 路由逻辑 |
| `context_window.py` | 模型上下文窗口大小查询 |
| `patches.py` | Provider 兼容性补丁（ccproxy、OpenRouter reasoning 等） |

## 关键设计

### 短名映射

`MODELS` 字典提供模型短名到 `(model_id, provider)` 的映射。同一短名可跨 provider 存在，`get_models_for_provider()` 按 provider 过滤。

### 自动配置

`_apply_auto_config()` 根据 provider 和模型自动启用特性：
- Anthropic: extended thinking（自适应或固定预算）
- OpenAI: reasoning effort
- Google GenAI: include_thoughts
- Ollama: reasoning 分离

### Provider 路由

第三方 provider 通过 OpenAI/Anthropic 兼容 API 路由，自动设置 `base_url` 和 `api_key`。

## 上下文窗口

`context_window.py` 从模型元数据获取上下文窗口大小，用于中间件触发阈值计算（如 ContextEditing 在 50% 上下文窗口时触发）。
