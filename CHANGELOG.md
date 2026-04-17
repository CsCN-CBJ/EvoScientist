# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 版本列表

- [v0.2.0 (2026-04-17)](#v020-2026-04-17) - 学术记忆注入：writing-agent 和 planner-agent 接入 ROME 学术记忆
- [v0.1.0 (2026-04-17)](#v010-2026-04-17) - 初始版本

---

## v0.2.0 (2026-04-17)

### ✨ 新增功能

- **📚 学术记忆注入** - writing-agent 和 planner-agent 可自动读取 ROME 产出的学术记忆文件（TASTE.md / WRITER.md / METHODOLOGY.md），注入 system prompt，使其具备品味感知的写作风格和有方法论的创意生成能力
- **🗂️ 独立学术记忆目录** - `EvoScientist/academic_memory/<category>/` 存放从 ROME 复制的记忆文件，与运行时 memory 完全隔离
- **⚙️ 可选配置** - 通过 `academic_memory_dir` 和 `academic_memory_category` 配置项启用；未配置时行为与原版完全一致，零回归

---

## [0.1.0] - 2026-04-17

### Added
- 架构文档（`docs/architecture/`）：overview、agent-core、backends、channels、cli、llm、mcp、middleware、skills-and-tools、stream
- 配置文档（`docs/config.md`）
- 部署文档（`docs/deployment.md`）
- 测试文档（`docs/testing.md`）
