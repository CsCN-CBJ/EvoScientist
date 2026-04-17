# 消息通道系统

## 模块职责

消息通道系统（`EvoScientist/channels/`）为 EvoScientist 提供 10 个消息平台的统一接入，让用户通过 Telegram、Discord、Slack 等与同一个 Agent 会话交互。

## 架构

详细架构、中间件管道、能力矩阵、安全模型和各通道部署指南见 [channels/README.md](../../EvoScientist/channels/README.md)。

## 核心模块

| 模块 | 职责 |
|------|------|
| `base.py` | Channel 抽象基类 — 就绪检查、重试策略、@提及过滤、格式降级、媒体处理、防抖、发送锁 |
| `capabilities.py` | ChannelCapabilities 冻结数据类 — 每个通道声明特性，框架自动适配 |
| `plugin.py` | ChannelPlugin 基类，含适配器插槽 |
| `mixins.py` | 可复用异步模式：WebhookMixin、WebSocketMixin、PollingMixin、TokenMixin |
| `config.py` | BaseChannelConfig — 共享配置字段 |
| `bus/` | MessageBus 异步事件总线，解耦通道与 Agent 核心 |
| `channel_manager.py` | 生命周期管理、健康监控、通道注册 |
| `consumer.py` | InboundConsumer — 工作池、per-chat 锁、会话去重、超时 |
| `retry.py` | RetryConfig — 指数退避重试 |
| `formatter.py` | UnifiedFormatter — Markdown 到平台格式转换 |

## 支持的通道

Telegram、Discord、Slack、Feishu、WeChat（企业微信/公众号）、DingTalk、QQ、Signal、Email、iMessage

## 消息处理流程

**入站**: 平台 SDK → `_on_message()` → RawIncoming → 中间件管道（去重→白名单→配对→群组历史→@提及） → InboundMessage → 队列 → 防抖合并 → MessageBus → InboundConsumer → Agent

**出站**: Agent 响应 → OutboundMessage → MessageBus → Dispatcher → Channel.send() → 格式转换 → 文本分块 → `_send_chunk()` → 重试

## 模块间交互

- **→ config/settings.py**: 读取通道配置
- **→ stt.py**: 语音消息转录（当 STT 启用时）
- **→ paths.py**: 媒体文件下载目录
- **← Agent 核心**: InboundConsumer 调用 Agent 处理入站消息
