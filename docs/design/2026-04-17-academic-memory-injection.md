# Academic Memory Injection 设计文档

**核心诉求：** EVO2 的 writing-agent 和 planner-agent 在推理时，自动读取 ROME 产出的学术记忆文件（TASTE.md / WRITER.md / METHODOLOGY.md），注入各自 system prompt，使 agent 具备品味感知的写作能力和有方法论的创意生成能力。

**日期：** 2026-04-17

---

## 背景

EvoScientist 已有通用 memory 层（`MEMORY.md`），记录用户 profile 和实验结论，每次 LLM 调用时注入 system prompt。但它缺乏"学术品味"层 —— 不知道好论文的写作风格，也不知道成功的研究方法论。

ROME 是独立项目，具备学术学习能力，产出以下文件：
- `memory/<category>/reviewer/TASTE.md` — 评审品味（好/差论文特征）
- `memory/<category>/writer/WRITER.md` — 写作风格记忆
- `memory/<category>/idea/METHODOLOGY.md` — 方法论知识

ROME 和 EVO2 是两个完全独立的项目，互不依赖。用户手动运行 ROME 的学习阶段（review/write/idea learn），产物写入 ROME 项目的 `memory/` 目录，再**复制**到 EVO2 项目的约定路径（`EvoScientist/academic_memory/<category>/`）。EVO2 不调用 ROME 代码，不引用 ROME 路径，只读取本项目目录内的文件。

**不做的代价**：writing-agent 写出的实验报告毫无学术品味，planner-agent 生成的创意缺乏方法论根基，两者都是"blind" LLM，浪费了 ROME 积累的知识。

---

## 方案

### 选择：在 `subagent.yaml` 声明 + `memory.py` 读取注入

**方案 A（纯 YAML）**：YAML 直接写死文件路径，middleware 统一注入给所有 agent。
- ❌ 无法区分 agent 类型，会给 code-agent 也注入写作风格，浪费 token

**方案 B（YAML 声明 + middleware 按 agent 过滤）** ✅ 选此方案
- `subagent.yaml` 每个 agent 声明 `academic_memory` 列表
- `EvoMemoryMiddleware` 接收 agent 名称，在 `modify_request` 时读取对应文件追加注入
- 改动量小：`memory.py` ~30 行，`subagent.yaml` ~10 行，工厂函数签名兼容扩展

**方案 C（新建独立 middleware）**：单独写 `AcademicMemoryMiddleware`。
- ❌ 代码复用差，backend 管理重复

### 关键设计决策

1. **注入位置**：追加在 `MEMORY_INJECTION_TEMPLATE` 之后，独立 `<academic_memory>` XML tag，与 MEMORY.md 区分
2. **路径规范**：academic memory 文件存放于 EVO2 项目内 `EvoScientist/academic_memory/<category>/`；路径通过配置传入，与 MEMORIES_DIR 分离
3. **文件缺失报错**：`academic_memory_dir` 已配置时，`academic_memory_files` 中列出的文件若不存在，抛出 `FileNotFoundError`，明确提示用户需先运行 ROME 学习阶段并复制产物
4. **未配置时跳过**：`academic_memory_dir` 未配置（`None`）→ 完全跳过注入，不报错，向后兼容
5. **category 感知**：middleware 构造时传入 `category`，从正确子目录读取文件

---

## 功能范围

### 包含
- `subagent.yaml`：writing-agent 声明注入 `TASTE.md` + `WRITER.md`；planner-agent 声明注入 `METHODOLOGY.md`
- `EvoMemoryMiddleware.__init__`：新增 `academic_memory_dir` 和 `agent_name` 参数
- `EvoMemoryMiddleware.modify_request`：读取对应文件，追加 `<academic_memory>` 注入
- `create_memory_middleware` 工厂函数：透传新参数
- `EvoScientist.py`：创建 middleware 时传入 `agent_name`（从 subagent config 读取）
- 单元测试：`tests/test_academic_memory.py`

### 不包含（本次迭代）
- ROME 学习阶段的调用（用户手动触发 ROME，产物放到约定路径）
- category 自动检测（本次 category 由用户配置）
- 动态热更新（文件变化后需重启）
- 对 research/code/debug/data-analysis agent 的注入

---

## 模块划分

### `EvoScientist/middleware/memory.py`

**变更**：`EvoMemoryMiddleware.__init__` 新增参数：
```python
academic_memory_dir: str | None = None   # ROME memory 根目录
agent_name: str | None = None            # 当前 agent 名（写入时按名过滤）
academic_memory_files: list[str] | None = None  # 从 subagent.yaml 读取的文件列表
```

`modify_request` 末尾追加：
```python
academic_content = self._read_academic_memory()
if academic_content:
    academic_injection = ACADEMIC_MEMORY_TEMPLATE.format(content=academic_content)
    new_system = append_to_system_message(new_system, academic_injection)
```

`_read_academic_memory()` 方法：遍历 `academic_memory_files`，逐一读取。
- `academic_memory_dir` 未配置 → 直接返回空字符串，不报错
- `academic_memory_dir` 已配置，文件不存在 → 抛出 `FileNotFoundError`（含文件路径），提示用户先复制 ROME 产物
- 所有文件读取成功 → 拼接返回，各文件间加分隔符

**接口契约**：
- 新参数全部可选，默认 `None`，不传时行为与原版完全一致（向后兼容）
- `ACADEMIC_MEMORY_TEMPLATE` 新增模块级常量

### `EvoScientist/subagent.yaml`

**变更**：writing-agent 和 planner-agent 增加 `academic_memory` 字段：
```yaml
writing-agent:
  academic_memory:
    - TASTE.md
    - WRITER.md

planner-agent:
  academic_memory:
    - METHODOLOGY.md
```

路径为相对文件名（如 `TASTE.md`），由 middleware 拼接 `academic_memory_dir / category / filename`。

### `EvoScientist/EvoScientist.py`

**变更**：`create_memory_middleware` 调用处，从 subagent config 解析 `academic_memory` 列表和 agent 名，传给 middleware。变更集中在 `_get_default_middleware()` 和 `create_cli_agent()` 函数，各约 5 行。

### `EvoScientist/config/settings.py`

**变更**（可选）：新增 `academic_memory_dir` 和 `academic_memory_category` 配置项，供 `create_memory_middleware` 读取。若不配置，academic memory 功能完全跳过，不报错。

---

## 测试与验收

### 单元测试覆盖范围（`tests/test_academic_memory.py`）

- `_read_academic_memory`：`academic_memory_dir` 未配置时返回空字符串（不报错）
- `_read_academic_memory`：`academic_memory_dir` 配置，文件不存在 → 抛出 `FileNotFoundError`
- `_read_academic_memory`：单文件读取成功，返回内容
- `_read_academic_memory`：多文件读取成功，内容拼接，含分隔符
- `modify_request`：无 academic memory（未配置）时，注入内容与原版一致（向后兼容）
- `modify_request`：有 academic memory 时，system prompt 中含 `<academic_memory>` 段

测试风格：纯函数 mock（参照现有 `test_memory_merge.py`），mock backend `.download_files()` 返回，无真实文件系统依赖。

### E2E 测试场景

- 场景 1：`academic_memory_dir` 未配置 → 系统正常启动，writing-agent 行为与原版无异
- 场景 2：`academic_memory_dir` 配置，文件不存在 → 启动时抛出 `FileNotFoundError`，提示用户复制 ROME 产物
- 场景 3：`academic_memory_dir` 配置，`WRITER.md` 存在 → writing-agent system prompt 中出现 `<academic_memory>` 内容
- 场景 4：`METHODOLOGY.md` 存在 → planner-agent system prompt 含方法论内容；code-agent system prompt 不含

### 验收标准

- [ ] `uv run pytest tests/test_academic_memory.py` 全部通过（含 FileNotFoundError 场景）
- [ ] `uv run ruff check .` 无新增 lint 错误
- [ ] `academic_memory_dir` 未配置时，所有现有测试（~890）全部通过
- [ ] `academic_memory_dir` 配置但文件缺失时，启动明确报 `FileNotFoundError` 含文件路径
- [ ] writing-agent system prompt 含 `<academic_memory>`，其他 4 个 agent 不含

---

## 风险与假设

| 假设 | 风险 | 应对 |
|------|------|------|
| academic memory 文件为 UTF-8 纯文本 | 编码异常 → 注入失败 | `_read_academic_memory` 捕获 decode 异常，转为带路径信息的 `ValueError` 抛出 |
| `academic_memory_files` 路径可信（来自 subagent.yaml） | 路径遍历攻击 | 文件名仅允许纯文件名（不含 `/` 或 `..`），middleware 构造时校验 |
| middleware 知道当前 agent 名 | agent 名未传入时无法过滤 | 未传 `agent_name` → 跳过注入，不崩溃 |
| 用户已运行 ROME 并复制产物 | 文件不存在 → `FileNotFoundError` 阻断启动 | 错误信息明确提示需复制哪个文件到哪个路径 |
| `modify_request` 调用时 backend 已初始化 | backend 为 None 时崩溃 | `_read_academic_memory` 用标准库 `pathlib` 直接读文件，不依赖 agent backend |
