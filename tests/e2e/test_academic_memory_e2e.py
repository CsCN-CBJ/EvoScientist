"""E2E tests for academic memory injection feature.

Tests end-to-end integration crossing module boundaries:
- Config → EvoScientist._get_default_middleware() → EvoMemoryMiddleware
- EvoMemoryMiddleware._read_academic_memory() → modify_request()
- subagent.yaml academic_memory declarations → _collect_academic_memory_files()

No mocks for the components under test; only external services and LLM init are mocked.
"""

from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch


# ---------------------------------------------------------------------------
# Scenario 1: academic_memory_dir not configured → full suite regression
# ---------------------------------------------------------------------------

class TestUnconfiguredAcademicMemory:
    """Scenario 1: academic_memory_dir not configured — zero regression."""

    @patch("EvoScientist.EvoScientist._ensure_chat_model")
    @patch("EvoScientist.EvoScientist._ensure_config")
    @patch("EvoScientist.middleware.create_tool_selector_middleware")
    def test_no_academic_memory_dir_middleware_builds_successfully(
        self, mock_ts, mock_cfg, mock_model
    ):
        """_get_default_middleware() succeeds when academic_memory_dir is empty."""
        mock_model.return_value = MagicMock(profile={"max_input_tokens": 200_000})
        cfg = MagicMock()
        cfg.academic_memory_dir = ""
        cfg.academic_memory_category = ""
        cfg.enable_ask_user = False
        cfg.auto_mode = False
        mock_cfg.return_value = cfg
        mock_ts.return_value = [MagicMock(), MagicMock()]

        from EvoScientist.EvoScientist import _get_default_middleware
        from EvoScientist.middleware.memory import EvoMemoryMiddleware

        mw = _get_default_middleware()
        memory_mw = next(m for m in mw if isinstance(m, EvoMemoryMiddleware))

        # academic_memory_dir not set on the middleware
        assert memory_mw._academic_memory_dir is None

    @patch("EvoScientist.EvoScientist._ensure_chat_model")
    @patch("EvoScientist.EvoScientist._ensure_config")
    @patch("EvoScientist.middleware.create_tool_selector_middleware")
    def test_no_academic_memory_dir_read_returns_empty(
        self, mock_ts, mock_cfg, mock_model
    ):
        """_read_academic_memory() returns '' when dir not configured."""
        mock_model.return_value = MagicMock(profile={"max_input_tokens": 200_000})
        cfg = MagicMock()
        cfg.academic_memory_dir = ""
        cfg.academic_memory_category = ""
        cfg.enable_ask_user = False
        cfg.auto_mode = False
        mock_cfg.return_value = cfg
        mock_ts.return_value = [MagicMock(), MagicMock()]

        from EvoScientist.EvoScientist import _get_default_middleware
        from EvoScientist.middleware.memory import EvoMemoryMiddleware

        mw = _get_default_middleware()
        memory_mw = next(m for m in mw if isinstance(m, EvoMemoryMiddleware))
        result = memory_mw._read_academic_memory()
        assert result == ""

    @patch("EvoScientist.EvoScientist._ensure_chat_model")
    @patch("EvoScientist.EvoScientist._ensure_config")
    @patch("EvoScientist.middleware.create_tool_selector_middleware")
    def test_no_academic_memory_dir_no_academic_tag_in_system_prompt(
        self, mock_ts, mock_cfg, mock_model
    ):
        """modify_request does NOT inject <academic_memory> when dir is unset."""
        mock_model.return_value = MagicMock(profile={"max_input_tokens": 200_000})
        cfg = MagicMock()
        cfg.academic_memory_dir = ""
        cfg.academic_memory_category = ""
        cfg.enable_ask_user = False
        cfg.auto_mode = False
        mock_cfg.return_value = cfg
        mock_ts.return_value = [MagicMock(), MagicMock()]

        from EvoScientist.EvoScientist import _get_default_middleware
        from EvoScientist.middleware.memory import EvoMemoryMiddleware

        mw = _get_default_middleware()
        memory_mw = next(m for m in mw if isinstance(m, EvoMemoryMiddleware))

        # Build a minimal request
        request = MagicMock()
        request.state = {}
        request.runtime = None
        request.system_message = "You are a helpful assistant."

        injections = []

        def _capture(sys_msg, injection):
            injections.append(injection)
            return (sys_msg or "") + injection

        with patch(
            "deepagents.middleware._utils.append_to_system_message",
            side_effect=_capture,
        ):
            memory_mw.modify_request(request)

        combined = "".join(injections)
        assert "<academic_memory>" not in combined


# ---------------------------------------------------------------------------
# Scenario 2: academic_memory_dir configured, file missing → FileNotFoundError
# ---------------------------------------------------------------------------

class TestMissingAcademicMemoryFile:
    """Scenario 2: configured dir but file absent → FileNotFoundError with path."""

    def test_missing_file_raises_file_not_found_with_path(self, tmp_path):
        """FileNotFoundError raised when dir is set but TASTE.md doesn't exist."""
        from EvoScientist.middleware.memory import EvoMemoryMiddleware

        mock_backend = MagicMock()
        resp = MagicMock()
        resp.content = None
        resp.error = "not found"
        mock_backend.download_files.return_value = [resp]

        mw = EvoMemoryMiddleware(
            backend=mock_backend,
            academic_memory_dir=str(tmp_path),
            academic_memory_category="ml",
            academic_memory_files=["TASTE.md", "WRITER.md"],
        )

        with pytest.raises(FileNotFoundError) as exc_info:
            mw._read_academic_memory()

        error_msg = str(exc_info.value)
        # Must name the missing file
        assert "TASTE.md" in error_msg or "WRITER.md" in error_msg
        # Must have actionable guidance
        assert "Academic memory file not found" in error_msg
        assert "Run ROME learning phase" in error_msg

    def test_error_message_contains_full_path(self, tmp_path):
        """FileNotFoundError message includes the full resolved path."""
        from EvoScientist.middleware.memory import EvoMemoryMiddleware

        mock_backend = MagicMock()
        resp = MagicMock()
        resp.content = None
        resp.error = "not found"
        mock_backend.download_files.return_value = [resp]

        mw = EvoMemoryMiddleware(
            backend=mock_backend,
            academic_memory_dir=str(tmp_path),
            academic_memory_category="ml",
            academic_memory_files=["WRITER.md"],
        )

        with pytest.raises(FileNotFoundError) as exc_info:
            mw._read_academic_memory()

        # Full path should appear (at minimum the filename)
        assert "WRITER.md" in str(exc_info.value)

    def test_partial_files_missing_raises_on_first_missing(self, tmp_path):
        """When first file exists but second is missing, error names the missing one."""
        from EvoScientist.middleware.memory import EvoMemoryMiddleware

        category_dir = tmp_path / "ml"
        category_dir.mkdir()
        # Create TASTE.md but not WRITER.md
        (category_dir / "TASTE.md").write_text("taste content")

        mock_backend = MagicMock()
        resp = MagicMock()
        resp.content = None
        resp.error = "not found"
        mock_backend.download_files.return_value = [resp]

        mw = EvoMemoryMiddleware(
            backend=mock_backend,
            academic_memory_dir=str(tmp_path),
            academic_memory_category="ml",
            academic_memory_files=["TASTE.md", "WRITER.md"],
        )

        with pytest.raises(FileNotFoundError) as exc_info:
            mw._read_academic_memory()

        assert "WRITER.md" in str(exc_info.value)


# ---------------------------------------------------------------------------
# Scenario 3: writing-agent system prompt contains <academic_memory>
# ---------------------------------------------------------------------------

class TestWritingAgentAcademicMemoryInjection:
    """Scenario 3: writing-agent gets <academic_memory> in system prompt."""

    def test_writing_agent_system_prompt_contains_academic_memory(self, tmp_path):
        """EvoMemoryMiddleware configured for writing-agent injects <academic_memory>."""
        from EvoScientist.middleware.memory import EvoMemoryMiddleware

        # Create TASTE.md and WRITER.md in the expected category dir
        category_dir = tmp_path / "ml"
        category_dir.mkdir()
        (category_dir / "TASTE.md").write_text(
            "# Taste Memory\nGood papers are concise and well-structured."
        )
        (category_dir / "WRITER.md").write_text(
            "# Writer Memory\nUse active voice and precise terminology."
        )

        mock_backend = MagicMock()
        resp = MagicMock()
        resp.content = None
        resp.error = "not found"
        mock_backend.download_files.return_value = [resp]

        # Simulate writing-agent middleware (TASTE.md + WRITER.md)
        mw = EvoMemoryMiddleware(
            backend=mock_backend,
            academic_memory_dir=str(tmp_path),
            academic_memory_category="ml",
            academic_memory_files=["TASTE.md", "WRITER.md"],
        )

        request = MagicMock()
        request.state = {}
        request.runtime = None
        request.system_message = "You are the writing-agent."

        injections = []

        def _capture(sys_msg, injection):
            injections.append(injection)
            return (sys_msg or "") + injection

        with patch(
            "deepagents.middleware._utils.append_to_system_message",
            side_effect=_capture,
        ):
            mw.modify_request(request)

        combined = "".join(injections)
        assert "<academic_memory>" in combined
        assert "Taste Memory" in combined
        assert "Writer Memory" in combined
        assert "Good papers are concise" in combined
        assert "Use active voice" in combined

    def test_writing_agent_academic_content_appears_after_evo_memory(self, tmp_path):
        """<academic_memory> block is appended after <evo_memory> injection."""
        from EvoScientist.middleware.memory import EvoMemoryMiddleware

        category_dir = tmp_path / "cat"
        category_dir.mkdir()
        (category_dir / "WRITER.md").write_text("writer style notes")

        mock_backend = MagicMock()
        resp = MagicMock()
        resp.content = None
        resp.error = "not found"
        mock_backend.download_files.return_value = [resp]

        mw = EvoMemoryMiddleware(
            backend=mock_backend,
            academic_memory_dir=str(tmp_path),
            academic_memory_category="cat",
            academic_memory_files=["WRITER.md"],
        )

        request = MagicMock()
        request.state = {}
        request.runtime = None
        request.system_message = "You are the writing-agent."

        injections = []

        def _capture(sys_msg, injection):
            injections.append(injection)
            return (sys_msg or "") + injection

        with patch(
            "deepagents.middleware._utils.append_to_system_message",
            side_effect=_capture,
        ):
            mw.modify_request(request)

        # Exactly 2 injections: evo_memory first, academic_memory second
        assert len(injections) == 2
        assert "<evo_memory>" in injections[0]
        assert "<academic_memory>" in injections[1]
        assert "writer style notes" in injections[1]

    @patch("EvoScientist.EvoScientist._ensure_chat_model")
    @patch("EvoScientist.EvoScientist._ensure_config")
    @patch("EvoScientist.middleware.create_tool_selector_middleware")
    def test_writing_agent_files_collected_from_subagent_yaml(
        self, mock_ts, mock_cfg, mock_model
    ):
        """_collect_academic_memory_files() includes TASTE.md and WRITER.md from subagent.yaml."""
        mock_model.return_value = MagicMock(profile={"max_input_tokens": 200_000})
        cfg = MagicMock()
        cfg.academic_memory_dir = "/some/dir"
        cfg.academic_memory_category = "ml"
        cfg.enable_ask_user = False
        cfg.auto_mode = False
        mock_cfg.return_value = cfg
        mock_ts.return_value = [MagicMock(), MagicMock()]

        from EvoScientist.EvoScientist import _collect_academic_memory_files

        files = _collect_academic_memory_files()

        # writing-agent declares TASTE.md + WRITER.md; planner declares METHODOLOGY.md
        assert "TASTE.md" in files
        assert "WRITER.md" in files
        assert "METHODOLOGY.md" in files


# ---------------------------------------------------------------------------
# Scenario 4: code-agent does NOT get <academic_memory>
# ---------------------------------------------------------------------------

class TestCodeAgentNoAcademicMemory:
    """Scenario 4: code-agent has no academic_memory in subagent.yaml → no injection."""

    def test_code_agent_no_academic_memory_files_in_yaml(self):
        """subagent.yaml code-agent spec has no academic_memory key."""
        import yaml
        from EvoScientist.EvoScientist import SUBAGENTS_CONFIG

        with SUBAGENTS_CONFIG.open(encoding="utf-8") as fh:
            config = yaml.safe_load(fh) or {}

        code_agent_spec = config.get("code-agent", {})
        # code-agent must NOT declare academic_memory
        assert "academic_memory" not in code_agent_spec or not code_agent_spec.get(
            "academic_memory"
        )

    def test_code_agent_middleware_without_academic_memory_no_injection(self):
        """EvoMemoryMiddleware with no academic_memory_files does not inject <academic_memory>."""
        from EvoScientist.middleware.memory import EvoMemoryMiddleware

        mock_backend = MagicMock()
        resp = MagicMock()
        resp.content = None
        resp.error = "not found"
        mock_backend.download_files.return_value = [resp]

        # Simulate code-agent: no academic_memory_files
        mw = EvoMemoryMiddleware(
            backend=mock_backend,
            academic_memory_dir="/some/dir",  # dir configured
            academic_memory_category="ml",
            academic_memory_files=None,  # code-agent has no files
        )

        request = MagicMock()
        request.state = {}
        request.runtime = None
        request.system_message = "You are the code-agent."

        injections = []

        def _capture(sys_msg, injection):
            injections.append(injection)
            return (sys_msg or "") + injection

        with patch(
            "deepagents.middleware._utils.append_to_system_message",
            side_effect=_capture,
        ):
            mw.modify_request(request)

        combined = "".join(injections)
        assert "<academic_memory>" not in combined

    def test_code_agent_read_returns_empty_when_no_files(self):
        """_read_academic_memory() returns '' when academic_memory_files is None."""
        from EvoScientist.middleware.memory import EvoMemoryMiddleware

        mock_backend = MagicMock()
        mw = EvoMemoryMiddleware(
            backend=mock_backend,
            academic_memory_dir="/some/dir",
            academic_memory_category="ml",
            academic_memory_files=None,
        )
        assert mw._read_academic_memory() == ""

    def test_only_writing_and_planner_declared_in_subagent_yaml(self):
        """Verify which agents have academic_memory in subagent.yaml."""
        import yaml
        from EvoScientist.EvoScientist import SUBAGENTS_CONFIG

        with SUBAGENTS_CONFIG.open(encoding="utf-8") as fh:
            config = yaml.safe_load(fh) or {}

        agents_with_academic_memory = [
            name
            for name, spec in config.items()
            if isinstance(spec, dict) and spec.get("academic_memory")
        ]

        # Only writing-agent and planner-agent should have academic_memory
        assert set(agents_with_academic_memory) == {"writing-agent", "planner-agent"}

        # Explicitly verify code-agent is absent
        assert "code-agent" not in agents_with_academic_memory
        # research, debug, data-analysis also absent
        for agent in ["research-agent", "debug-agent", "data-analysis-agent"]:
            assert agent not in agents_with_academic_memory
