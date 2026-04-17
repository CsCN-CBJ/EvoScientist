# Academic Memory Injection 集成测试报告

**日期：** 2026-04-17
**设计文档：** [docs/design/2026-04-17-academic-memory-injection.md](./2026-04-17-academic-memory-injection.md)

---

## 测试结果概览

- 单元测试（`tests/test_academic_memory.py`）：12/12 pass ✅
- E2E 测试（`tests/e2e/test_academic_memory_e2e.py`）：13/13 pass ✅
- 回归测试（全量 `uv run pytest`）：1491 passed, 10 skipped ✅
- Lint（`uv run ruff check .`）：All checks passed ✅

---

## 功能验证

### 场景 1：academic_memory_dir 未配置 → 零回归

- **测试用例：** `test_no_academic_memory_dir_middleware_builds_successfully`, `test_no_academic_memory_dir_read_returns_empty`, `test_no_academic_memory_dir_no_academic_tag_in_system_prompt`
- **测试方法：** 以 `academic_memory_dir=""` 构建 config mock，调用 `_get_default_middleware()`，取出 `EvoMemoryMiddleware` 实例，验证 `_academic_memory_dir is None`；调用 `_read_academic_memory()` 验证返回 `""`；调用 `modify_request()` 捕获所有 `append_to_system_message` 注入，验证无 `<academic_memory>` 出现
- **通过判定：** `memory_mw._academic_memory_dir is None`；`result == ""`；`"<academic_memory>" not in combined`
- **结果：** ✅ 通过（全量回归 1491 pass）

### 场景 2：academic_memory_dir 配置但文件缺失 → FileNotFoundError 含路径

- **测试用例：** `test_missing_file_raises_file_not_found_with_path`, `test_error_message_contains_full_path`, `test_partial_files_missing_raises_on_first_missing`
- **测试方法：** 以真实 `tmp_path` 作为 `academic_memory_dir`（不创建实际文件），调用 `_read_academic_memory()`，断言抛出 `FileNotFoundError`。子测试：第一个文件存在，第二个不存在时，错误信息应点名缺失的那个文件
- **通过判定：** `pytest.raises(FileNotFoundError)`；`str(exc_info.value)` 含 `"TASTE.md"` 或 `"WRITER.md"`；含 `"Academic memory file not found"` 和 `"Run ROME learning phase"`
- **结果：** ✅ 通过

### 场景 3：writing-agent system prompt 含 `<academic_memory>`

- **测试用例：** `test_writing_agent_system_prompt_contains_academic_memory`, `test_writing_agent_academic_content_appears_after_evo_memory`, `test_writing_agent_files_collected_from_subagent_yaml`
- **测试方法：**
  1. 创建真实文件 `TASTE.md`、`WRITER.md` 于 `tmp_path/ml/`，构建 `EvoMemoryMiddleware(academic_memory_files=["TASTE.md","WRITER.md"])`，调用 `modify_request()`，捕获所有注入，断言 `<academic_memory>` 和文件内容出现
  2. 捕获 `append_to_system_message` 调用顺序，断言第 1 次注入含 `<evo_memory>`，第 2 次含 `<academic_memory>`
  3. 调用真实 `_collect_academic_memory_files()` 读取项目 `subagent.yaml`，断言返回列表含 `TASTE.md`、`WRITER.md`、`METHODOLOGY.md`
- **通过判定：** `"<academic_memory>" in combined`；文件内容字符串在注入中可见；`len(injections) == 2` 且顺序正确；`"TASTE.md" in files`
- **结果：** ✅ 通过

### 场景 4：code-agent system prompt 不含 `<academic_memory>`

- **测试用例：** `test_code_agent_no_academic_memory_files_in_yaml`, `test_code_agent_middleware_without_academic_memory_no_injection`, `test_code_agent_read_returns_empty_when_no_files`, `test_only_writing_and_planner_declared_in_subagent_yaml`
- **测试方法：**
  1. 直接读取项目 `subagent.yaml`，断言 `code-agent` 条目无 `academic_memory` 字段
  2. 构建 `EvoMemoryMiddleware(academic_memory_dir="/some/dir", academic_memory_files=None)`（模拟 code-agent），调用 `modify_request()`，断言注入中无 `<academic_memory>`
  3. 读取 `subagent.yaml`，断言只有 `writing-agent` 和 `planner-agent` 声明了 `academic_memory`，`code-agent`、`research-agent`、`debug-agent`、`data-analysis-agent` 均未声明
- **通过判定：** `"academic_memory" not in code_agent_spec`；`"<academic_memory>" not in combined`；`set(agents_with_academic_memory) == {"writing-agent", "planner-agent"}`
- **结果：** ✅ 通过

---

## 设计文档未覆盖的发现

- **`_collect_academic_memory_files()` 收集全量文件**：设计文档描述 middleware 按 agent 名过滤，但实际实现是全量收集所有 agent 的 `academic_memory` 文件，传给单个 `EvoMemoryMiddleware` 实例（主 agent 共用）。per-agent 过滤通过在 `subagent.yaml` 不声明 `academic_memory` 实现，而非 middleware 运行时过滤。功能结果正确（code-agent 确实不注入），但机制与设计文档描述略有偏差。
- **`academic_memory_files=None` vs `[]` 均返回 `""`**：两种情况均安全，无需区分。已测试。

## 需要用户手动验证的部分

- [ ] 真实运行 ROME 学习阶段，将产物复制到 `EvoScientist/academic_memory/<category>/`，启动 EvoSci，观察 writing-agent 实际系统提示是否包含 TASTE.md / WRITER.md 内容

---

## 验收标准核对

- [x] `uv run pytest tests/test_academic_memory.py` 全部通过（12/12）✅
- [x] `uv run ruff check .` 无新增 lint 错误 ✅
- [x] `academic_memory_dir` 未配置时，所有现有测试（1491）全部通过 ✅
- [x] `academic_memory_dir` 配置但文件缺失时，明确报 `FileNotFoundError` 含文件路径 ✅
- [x] writing-agent system prompt 含 `<academic_memory>`，其他 agent 不含（code/research/debug/data-analysis 均未声明） ✅
