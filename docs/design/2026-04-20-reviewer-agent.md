# Design: Reviewer-Agent for EVO2

**日期：** 2026-04-20
**需求：** 为 writing-agent 添加 reviewer-agent，最多 review 3 轮，支持多 reviewer persona 并行审稿

## 核心诉求

writing-agent 写完论文后，reviewer-agent 对论文进行结构化审稿。reviewer-agent 自行启动多个子 agent（每个采用不同 TASTE persona），汇总审稿意见后写入文件。writer 根据反馈修改，最多迭代 3 轮。

## 方案

### 新增 reviewer-agent（subagent.yaml）

在 `subagent.yaml` 中新增 `reviewer-agent` 定义：

```yaml
reviewer-agent:
  description: "Review a paper draft with multiple reviewer personas. Each persona reads its own TASTE file, reviews independently, then reviews are merged into a panel verdict."
  tools: [think_tool]
  skills: ["/skills/"]
  academic_memory: []
  system_prompt: |
    You are the reviewer-agent coordinator. Your job is to review a paper draft by:
    1. Reading the paper from the specified file path
    2. Discovering available reviewer TASTE files in academic_memory/system/reviewers/
    3. For each TASTE file, launching a sub-task using the `task` tool to review the paper from that persona's perspective
    4. Merging all reviews into a consolidated panel verdict
    5. Writing the merged review to the specified output file

    Sub-task invocation pattern:
    For each TASTE file (e.g., reviewerA/TASTE.md):
      task(subagent_type="reviewer-agent", description="Review /paper.md adopting the persona defined in /path/to/reviewers/reviewerA/TASTE.md. Output structured review only.")

    When acting as a single reviewer (sub-task), you MUST:
    1. Read and adopt the persona from the specified TASTE file
    2. Read the paper from the specified file path
    3. Output a structured review

    Review output format (strict, for each persona):
    ## Review by [Persona Name]

    ### Summary
    One-paragraph summary of the paper.

    ### Strengths
    - (numbered list)

    ### Weaknesses
    - (numbered list, each with severity: major/minor)

    ### Questions for Authors
    - (numbered list)

    ### Detailed Comments
    Section-by-section specific feedback with section references.

    ### Verdict
    One of: accept / minor-revision / major-revision / reject

    Panel merge output format:
    ## Panel Review - Round N

    ### Consensus Strengths
    - (merged from all reviewers)

    ### Consensus Weaknesses (sorted by severity)
    - (merged, deduplicated, with count of reviewers who raised each)

    ### Disagreement Points
    - (where reviewers disagreed)

    ### Questions for Authors
    - (merged, deduplicated)

    ### Detailed Comments
    (all reviewers' detailed comments, grouped by section)

    ### Panel Verdict
    One of: accept / minor-revision / major-revision / reject
    (based on majority vote; reject requires majority)

    ### Must-Fix Items
    Items that MUST be addressed before the next round.

    Rules:
    - Be critical, fair, and evidence-driven
    - Every weakness must reference a specific section/paragraph
    - Distinguish major issues from minor issues
    - Do not fabricate concerns; ground every point in the paper text
    - After round 3, provide a final verdict regardless of remaining issues
```

### 多 Reviewer Persona 机制

**TASTE 文件存放位置：** `EvoScientist/academic_memory/system/reviewers/`

```
academic_memory/system/reviewers/
├── reviewerA/TASTE.md    # novelty/correctness 视角
├── reviewerB/TASTE.md    # deployment/reliability 视角
├── reviewerC/TASTE.md    # evaluation/reproducibility 视角
└── ...                   # 新增 reviewer 只需加目录+TASTE.md
```

**发现机制：** reviewer-agent 作为 coordinator 时，扫描 `academic_memory/system/reviewers/*/TASTE.md` 路径，为每个 TASTE 文件启动一个并行 sub-task。

**扩展方式：** 新增 reviewer = 在 `reviewers/` 目录下新建子目录 + TASTE 文件，无需改 YAML 或 Python 代码。

**不通过 academic_memory 声明注入**：reviewer-agent 的 `academic_memory: []`，由 agent 自行读文件选择 persona，避免所有 TASTE 被强制注入 context。

### Review Log

每轮 review 结果写到和 paper.md 同目录下：

```
paper/
├── paper.md                  # 论文本体
├── review_round_1.md         # Round 1 panel review
├── review_round_2.md         # Round 2 panel review
└── review_round_3.md         # Round 3 panel review（如有）
```

Review log 永久保留，不删除。

**Review log 格式：**

```markdown
# Panel Review - Round 1

## Individual Reviews

### Review by Reviewer A (Analyst)
(完整审稿意见)

### Review by Reviewer B (Practitioner)
(完整审稿意见)

## Panel Verdict
(汇总意见)

### Consensus Strengths
- ...

### Consensus Weaknesses
- ...

### Must-Fix Items
- ...

### Panel Verdict: major-revision
```

### 新增 structured-writing 技能的 review 流程

修改 `EvoScientist/skills/structured-writing/SKILL.md`，在 Phase B 的 Step B4 之后添加 review 循环：

```
Phase B: Node Execution
  Step B1-B3: (不变)
  Step B4: Final Review (self-check)
  Step B5: Review Loop (NEW)
    for round 1..3:
      1. 主 agent 调用 reviewer-agent：
         task(subagent_type="reviewer-agent",
              description="Review /paper/paper.md. Write panel review to /paper/review_round_N.md. Round N.")
      2. reviewer-agent 作为 coordinator：
         a. 扫描 academic_memory/system/reviewers/*/TASTE.md
         b. 为每个 TASTE 并行启动 sub-task
         c. 汇总为 panel verdict
         d. 写入 /paper/review_round_N.md
      3. 主 agent 读取 review_round_N.md
      4. 如果 panel verdict = accept 或 minor-revision 且无 major → 停止
      5. 主 agent 调用 writing-agent 修改论文：
         task(subagent_type="writing-agent",
              description="Revise /paper/paper.md based on review at /paper/review_round_N.md")
    end
  Step B6: Clean Up（保留 review logs，不删除）
```

### 3 轮迭代规则

| 轮次 | reviewer 行为 | writer 行为 |
|------|-------------|------------|
| Round 1 | 全面审稿，覆盖所有维度 | 针对所有 major weaknesses 修改 |
| Round 2 | 检查 Round 1 的问题是否解决，发现新问题 | 针对遗留 major + minor 修改 |
| Round 3 | 最终确认，不再发现新问题 | 只改 must-fix items |

**提前终止条件：**
- panel verdict = `accept` → 停止
- panel verdict = `minor-revision` 且无 major weaknesses → 停止
- 3 轮用完 → 强制停止，输出最终 verdict

### 主 Agent 编排

主 Agent 负责 review 循环的编排：
1. writing-agent 完成初稿 → 写到 `/paper/paper.md`
2. 主 Agent 调用 reviewer-agent → reviewer-agent 自行启动多个子 agent 并行审稿
3. reviewer-agent 汇总意见，写入 `/paper/review_round_N.md`
4. 主 Agent 读取 verdict，决定是否继续
5. 如需修改，主 Agent 调用 writing-agent 修订

## 功能范围

### 包含

1. `subagent.yaml` — 新增 reviewer-agent 定义
2. `EvoScientist/skills/structured-writing/SKILL.md` — 添加 review 循环步骤
3. `EvoScientist/academic_memory/system/reviewers/` — 从 ROME 复制 reviewer TASTE 文件
4. `EvoScientist/prompts.py` — Step 5 添加 review 循环指导

### 不包含（本次迭代）

- 不修改 Python 代码
- 不实现 panel 合议 LLM 调用（ROME 的 review chair 模式）——由 reviewer-agent 自行汇总
- 不实现 reviewer QA 对话（ROME 的 `reviewer_qa_with_trace()`）
- 不实现 reviewer learn pipeline
- reviewer 递归嵌套深度限制为 1 层（coordinator → sub-tasks，sub-tasks 不可再启动子 agent）

## 文件变更清单

| 文件 | 变更类型 | 变更内容 |
|------|---------|---------|
| `EvoScientist/subagent.yaml` | 修改 | 新增 reviewer-agent 定义 |
| `EvoScientist/skills/structured-writing/SKILL.md` | 修改 | Step B5 添加 review 循环 |
| `EvoScientist/academic_memory/system/reviewers/reviewerA/TASTE.md` | 新增 | 从 ROME 复制 |
| `EvoScientist/academic_memory/system/reviewers/reviewerB/TASTE.md` | 新增 | 从 ROME 复制 |
| `EvoScientist/academic_memory/system/reviewers/reviewerC/TASTE.md` | 新增 | 从 ROME 复制 |
| `EvoScientist/prompts.py` | 修改 | Step 5 添加 review 循环指导 |

## 风险

1. **reviewer-agent 递归调用**：reviewer-agent 通过 `task` 工具启动子 reviewer，但子 reviewer 也是 reviewer-agent，可能导致无限递归 — 通过 system prompt 约束：sub-task 中不可再启动子 agent
2. **reviewer TASTE 质量**：当前 5 个 reviewer TASTE 内容相同（未分别 learn），审稿视角单一 — 后续运行 ROME reviewer learn 分别学习
3. **并行 sub-task 数量**：当前 5 个 TASTE 同时启动，token 消耗和 API 并发较大 — 可通过配置控制启用的 reviewer 数量
4. **论文产出目录**：从 `/paper.md` 改为 `/paper/paper.md`，需要同步更新 writing-agent 的输出路径
