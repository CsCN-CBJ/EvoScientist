# 技能与工具

## 模块职责

技能和工具系统为 Agent 提供可扩展的能力：内置工具（think、search）、技能系统（可安装的工作流包）、MCP 外部工具。

## 内置工具

| 工具 | 文件 | 说明 |
|------|------|------|
| think_tool | `tools/think.py` | 结构化反思，每步必选 |
| tavily_search | `tools/search.py` | Tavily 网页搜索（需 API Key） |
| skill_manager | `tools/skill_manager.py` | 技能安装/卸装/列表管理 |

## 技能系统

### 技能目录层级

| 层级 | 目录 | 优先级 | 权限 |
|------|------|--------|------|
| 项目本地 | `<workspace>/skills/` | 最高 | 读写 |
| 用户全局 | `~/.config/evoscientist/skills/` | 中 | 只读 |
| 内置 | `EvoScientist/skills/` | 最低 | 只读 |

### 技能管理

- CLI: `/install-skill <src>`、`/uninstall-skill <name>`、`/skills`
- 安装来源: 本地路径或 GitHub 仓库
- 每个技能包含 `SKILL.md` 描述文件

### 内置技能

`EvoScientist/skills/` 包含内置技能包：
- **skill-creator**: 创建新技能的技能
- **find-skills**: 发现和安装可用技能
- **structured-writing**: 自顶向下结构拆解+逐节点执行的论文写作技能（Phase A 结构拆解 → Phase B 逐节点写作 → Review 循环）

### 技能使用

子 Agent 在 system prompt 中声明 `skills: ["/skills/"]`，运行时可读取技能的 `SKILL.md` 获取工作流指导。主 Agent 的 system prompt 中也包含技能使用指引。

## 工具选择

当工具总数超过 26 时，`ConditionalToolSelectorMiddleware` 通过额外 LLM 调用自动选择相关工具子集，`think_tool` 和 `task` 始终包含。

## 模块间交互

- **→ backends.py**: MergedSkillsBackend 管理三层技能目录
- **→ middleware/tool_selector.py**: 自适应工具选择
- **→ mcp/**: MCP 工具注入到工具注册表
- **← Agent 核心**: 子 Agent 通过 `/skills/` 路径读取技能定义
