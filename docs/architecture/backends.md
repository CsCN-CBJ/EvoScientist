# 后端系统

## 模块职责

后端系统（`EvoScientist/backends.py`）为 Agent 提供文件操作和命令执行能力，同时确保沙盒安全性。

## 核心组件

### CustomSandboxBackend

继承 `LocalShellBackend`，增加了安全防护：

- **路径修正** — 自动纠正 LLM 常见的路径错误（如幻觉出的系统绝对路径 `/Users/.../project/file.py` → `./file.py`）
- **命令验证** — 阻止目录穿越（`../`）、危险命令（sudo/chmod/dd/shutdown 等）、绝对系统路径
- **超时增强** — 命令超时（默认 300s）时给出后台执行建议
- **虚拟路径转换** — `convert_virtual_paths_in_command()` 将虚拟路径转为相对路径

### MergedSkillsBackend

三层技能目录合并，高优先级覆盖低优先级同名技能：

| 优先级 | 目录 | 说明 | 权限 |
|--------|------|------|------|
| 1（最高）| workspace/skills/ | 项目本地 | 读写 |
| 2 | ~/.config/evoscientist/skills/ | 用户全局 | 只读 |
| 3（最低）| EvoScientist/skills/ | 内置 | 只读 |

读操作按优先级依次尝试；列表/搜索操作合并所有层级，高优先级同名覆盖；写操作只写入项目本地目录。

### ReadOnlyFilesystemBackend

只读文件系统后端，用于全局技能目录和内置技能目录。阻止所有写和编辑操作。

## CompositeBackend 路由

Agent 使用 `CompositeBackend` 将路径路由到不同后端：

| 路径前缀 | 后端 | 用途 |
|----------|------|------|
| `/skills/` | MergedSkillsBackend | 技能文件 |
| `/memories/` | FilesystemBackend（虚拟模式）| 记忆文件 |
| 其他 | CustomSandboxBackend | 工作空间文件和命令 |

## 安全模型

- 工作空间根目录外的路径操作被阻止
- 危险 shell 命令被拦截（sudo、chmod、mkfs、dd、shutdown 等）
- 目录穿越（`..`）被检测和阻止
- 命令输出截断为 100KB，超时 300 秒
- LLM 幻觉路径自动修正而非报错
