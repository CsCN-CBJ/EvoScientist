# structured-writing 技能设计文档

**核心诉求：** 为 writing-agent 提供自顶向下逐层拆解论文结构并逐节点执行的写作流程，替代现有固定模板+串行写法。

**日期：** 2026-04-20

## 背景

现有 EvoScientist 的写作流程依赖 `paper-writing` 外部技能，存在三个问题：

1. **固定模板**：Method 固定是"Overview→逐模块子节"，Experiments 固定是"对比→消融→demo"，不管论文内容如何结构已定好，无法自适应
2. **拆解深度不足**：最多到节的写作计划，段落层面只靠"一段一意"通用原则，缺少显式的修辞模式选择
3. **串行执行**：11 步严格串行，一个 agent 一步一步写完

用户期望的流程是：自顶向下不断拆解——先是大章节组织，然后每个章节内部是否需要子章节，如果不需要则规划段落间组织关系，如果需要则规划子章节间组织关系，再到段落里每句话的组织关系（总分分总、先挑战后方案等），全部规划好后再逐节点执行。

## 方案

创建 `structured-writing` 技能，内置到 `EvoScientist/skills/`，作为 writing-agent 的执行指南。

### 核心流程：两阶段

```
Phase A: Structure Decomposition（结构拆解）
    输入：研究内容（实验结果、方法描述、论文目标等）
    过程：自顶向下逐层拆解，输出结构树
    产出：structure.md（完整结构树）

Phase B: Node Execution（逐节点执行）
    输入：structure.md
    过程：深度优先遍历结构树，每个叶节点按其声明的修辞模式写作
    产出：各节点内容，最终组装为完整论文
```

### 结构树规范

结构树是一棵多叉树，每个节点包含：

```yaml
id: "1"                          # 唯一标识
level: chapter|section|subsection|paragraph  # 层级
title: "Introduction"            # 标题/主题
rhetorical_mode: null            # 非叶节点为 null
children: [...]                  # 子节点（可为空）
```

叶节点（paragraph 级别）额外包含：

```yaml
rhetorical_mode: "claim-evidence" # 修辞模式
key_points:                      # 该段要传达的关键点
  - "Existing methods fail on X"
  - "We propose Y to address X"
```

### 拆解规则

1. **章级（chapter）**：根据论文内容决定需要几个大章，不固定为 7 节
2. **节级（section）**：每章内部判断是否需要子节。一个核心创新可能不需要子节，三个模块就拆三个子节
3. **子节级（subsection）**：同上，按需拆分
4. **段落级（paragraph）**：每个叶节点必须声明修辞模式

### 修辞模式

不预设模板库。agent 在拆解到段落级时，根据内容需要自行选择修辞模式。SKILL.md 中给出常见模式作为参考（非强制）：

| 模式 | 适用场景 | 结构 |
|------|---------|------|
| claim-evidence | 提出论点后给证据 | 主张→证据→解释 |
| challenge-insight-solution | 引出问题后给方案 | 挑战→洞察→方案 |
| general-specific-general | 总分总 | 总述→分述→总结 |
| data-analysis-conclusion | 实验结果 | 数据→分析→结论 |
| chronological | 方法步骤 | 步骤1→步骤2→... |
| comparison | 对比分析 | A→B→对比→结论 |

agent 可以自创模式，只要在节点中声明清楚即可。

### 与现有系统的关系

- **不依赖 `paper-writing` 外部技能**：完全独立，内置到 `EvoScientist/skills/`
- **复用 writing-agent 的 system prompt**：技能通过 SKILL.md 被 writing-agent 读取，不修改 `subagent.yaml`
- **复用 academic memory 注入**：TASTE.md 和 WRITER.md 仍通过 middleware 注入，技能本身不处理
- **不修改任何 Python 代码**：纯 SKILL.md + references 文档

## 功能范围

### 包含

- `EvoScientist/skills/structured-writing/SKILL.md` — 核心流程规范
- `EvoScientist/skills/structured-writing/references/structure-spec.md` — 结构树规范详细说明
- `EvoScientist/skills/structured-writing/references/rhetorical-modes.md` — 修辞模式参考
- `EvoScientist/skills/structured-writing/references/decomposition-guide.md` — 拆解决策指南
- `EvoScientist/skills/structured-writing/references/writing-quality.md` — 写作质量检查清单

### 不包含（本次迭代）

- 不修改 `subagent.yaml`（writing-agent 声明仍指向 `/skills/`，运行时自动发现）
- 不实现多 agent 并行编排（单 agent 串行执行结构树）
- 不内置 LaTeX 模板或表格样式
- 不创建 reviewer/rebuttal 等配套技能
- 不修改 Python 代码

## 模块划分

单技能目录，文件边界清晰：

| 文件 | 职责 |
|------|------|
| `SKILL.md` | 技能入口：When to Use、两阶段流程、核心规则、质量检查 |
| `references/structure-spec.md` | 结构树的数据规范、节点字段、层级定义 |
| `references/rhetorical-modes.md` | 修辞模式参考（非强制），含示例 |
| `references/decomposition-guide.md` | 每层的拆解决策方法：何时拆子节、何时停止 |
| `references/writing-quality.md` | 每个节点写完后的质量自检清单 |

## 测试与验收

### 验收标准

- [ ] `EvoScientist/skills/structured-writing/` 目录存在，包含 SKILL.md 和 4 个 references 文件
- [ ] SKILL.md 定义了完整的两阶段流程（Structure Decomposition + Node Execution）
- [ ] 结构树规范支持 chapter/section/subsection/paragraph 四级，叶节点可声明修辞模式
- [ ] 不引用 `paper-writing` 技能，不依赖外部安装
- [ ] `pyproject.toml` 中 `skills/**/*` 通配符已覆盖此目录（无需修改）
- [ ] writing-agent 的 `skills: ["/skills/"]` 声明可自动发现此技能（无需修改代码）
- [ ] SKILL.md 中有明确的 When to Use / When NOT to Use
- [ ] 所有 reference 文件无 placeholder（TBD/TODO）

### 手动验证

- 启动 `EvoSci`，配置 `academic_memory_dir`，运行一次写作任务，观察 writing-agent 是否读取 `structured-writing/SKILL.md` 并按其流程执行

## 风险与假设

### 假设

1. writing-agent 的 `skills: ["/skills/"]` 声明会让它在运行时读取 `EvoScientist/skills/` 下的所有 SKILL.md——需验证 `MergedSkillsBackend` 的加载逻辑
2. agent 能按 SKILL.md 的指令完成结构拆解和逐节点写作，不需要 Python 代码层面的结构化支持
3. 单 agent 串行遍历结构树即可满足当前需求，无需并行编排

### 风险

1. **技能发现机制**：如果 writing-agent 只读取 workspace 级 skills 而忽略内置 skills，则需调整加载逻辑——需先验证
2. **agent 执行纪律**：自顶向下拆解后逐节点执行，agent 可能跳过拆解直接写——SKILL.md 中需要硬门控
3. **结构树持久化**：拆解结果写到哪里？如果写到工作空间文件，可能与其他技能冲突——建议写到 `/structure.md` 并在完成后删除
