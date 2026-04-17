# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.7] - 2026-04-XX

### Added
- Multi-provider LLM support: Anthropic, OpenAI, Google GenAI, MiniMax, NVIDIA, SiliconFlow, OpenRouter, ZhipuAI, Volcengine, DashScope, DeepSeek, Moonshot, Kimi Coding, Ollama, custom OpenAI/Anthropic endpoints
- 10 messaging channel integrations: Telegram, Discord, Slack, Feishu, WeChat, DingTalk, QQ, Signal, Email, iMessage
- MCP (Model Context Protocol) integration with tool routing and wildcard filtering
- EvoMemory v1.0: persistent memory with LLM-based extraction
- Adaptive tool selector middleware (threshold-based, per-turn tool selection)
- Context editing middleware (dynamic system prompt rewriting)
- Full-screen TUI and classic CLI interfaces
- 200+ predefined skills built in
- Human-in-the-loop action approval (HITL)
- Agent-initiated human clarification (AskUserMiddleware)
- OAuth sign-in support for CLI coding agent subscribers
- Speech-to-text transcription (faster-whisper)
- Session persistence with SQLite checkpointer

### Changed
- Default model updated to claude-sonnet-4-6
- MergedSkillsBackend now supports three-tier skill directory (workspace/global/built-in)

## [0.0.6] - 2026-03-13

### Added
- Initial public release
- 6 sub-agents: planner, research, code, debug, data-analysis, writing
- Scientific workflow: Intake → Plan → Execute → Evaluate → Write → Verify
- DeepAgents + LangChain + LangGraph framework foundation
