"""Tests for academic memory injection in EvoMemoryMiddleware.

Covers:
- _read_academic_memory: unconfigured dir → empty string
- _read_academic_memory: configured dir, file missing → FileNotFoundError
- _read_academic_memory: single file read success
- _read_academic_memory: multiple files concatenated with separator
- modify_request: backward compatible when unconfigured
- modify_request: injects <academic_memory> block when configured
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from EvoScientist.middleware.memory import (
    EvoMemoryMiddleware,
)

# ---------------------------------------------------------------------------
# Helpers to build a minimal EvoMemoryMiddleware without real backend
# ---------------------------------------------------------------------------


def _make_middleware(
    academic_memory_dir: str | None = None,
    academic_memory_category: str | None = None,
    academic_memory_files: list[str] | None = None,
) -> EvoMemoryMiddleware:
    """Create middleware with a mock backend, only testing academic memory."""
    mock_backend = MagicMock()
    # Simulate MEMORY.md not found (download returns empty)
    mock_response = MagicMock()
    mock_response.content = None
    mock_response.error = "not found"
    mock_backend.download_files.return_value = [mock_response]
    return EvoMemoryMiddleware(
        backend=mock_backend,
        academic_memory_dir=academic_memory_dir,
        academic_memory_category=academic_memory_category,
        academic_memory_files=academic_memory_files,
    )


def _make_request(system_message: str = "You are a helpful assistant."):
    """Build a minimal ModelRequest-like object for modify_request tests."""
    from unittest.mock import MagicMock

    request = MagicMock()
    request.state = {}
    request.runtime = None
    request.system_message = system_message

    # Make override() return a new mock with the new system_message stored
    def _override(**kwargs):
        new_req = MagicMock()
        new_req.system_message = kwargs.get("system_message", system_message)
        return new_req

    request.override.side_effect = _override
    return request


# ---------------------------------------------------------------------------
# Tests for _read_academic_memory
# ---------------------------------------------------------------------------


class TestReadAcademicMemory:
    """Unit tests for EvoMemoryMiddleware._read_academic_memory."""

    def test_unconfigured_dir_returns_empty_string(self):
        """When academic_memory_dir is None, return '' without error."""
        mw = _make_middleware(academic_memory_dir=None)
        result = mw._read_academic_memory()
        assert result == ""

    def test_configured_dir_missing_file_raises_file_not_found(self, tmp_path):
        """When dir is set but the file doesn't exist, raise FileNotFoundError."""
        mw = _make_middleware(
            academic_memory_dir=str(tmp_path),
            academic_memory_category="ml",
            academic_memory_files=["TASTE.md"],
        )
        with pytest.raises(FileNotFoundError) as exc_info:
            mw._read_academic_memory()
        # Error message must contain the file path
        assert "TASTE.md" in str(exc_info.value)
        assert "Academic memory file not found" in str(exc_info.value)
        assert "Run ROME learning phase" in str(exc_info.value)

    def test_single_file_read_success(self, tmp_path):
        """Single file is read and its content returned."""
        category_dir = tmp_path / "ml"
        category_dir.mkdir()
        taste_file = category_dir / "TASTE.md"
        taste_file.write_text("# Taste Memory\nGood papers have clear experiments.")

        mw = _make_middleware(
            academic_memory_dir=str(tmp_path),
            academic_memory_category="ml",
            academic_memory_files=["TASTE.md"],
        )
        result = mw._read_academic_memory()
        assert "Taste Memory" in result
        assert "Good papers have clear experiments." in result

    def test_multiple_files_concatenated_with_separator(self, tmp_path):
        """Multiple files are joined with a separator between them."""
        category_dir = tmp_path / "nlp"
        category_dir.mkdir()
        (category_dir / "TASTE.md").write_text("taste content")
        (category_dir / "WRITER.md").write_text("writer content")

        mw = _make_middleware(
            academic_memory_dir=str(tmp_path),
            academic_memory_category="nlp",
            academic_memory_files=["TASTE.md", "WRITER.md"],
        )
        result = mw._read_academic_memory()
        assert "taste content" in result
        assert "writer content" in result
        # There must be some separator between them
        taste_pos = result.index("taste content")
        writer_pos = result.index("writer content")
        between = result[taste_pos + len("taste content"):writer_pos]
        assert len(between.strip()) > 0, "Expected a separator between files"

    def test_no_files_list_returns_empty_string(self, tmp_path):
        """When academic_memory_files is None (even if dir is set), return ''."""
        mw = _make_middleware(
            academic_memory_dir=str(tmp_path),
            academic_memory_category="ml",
            academic_memory_files=None,
        )
        result = mw._read_academic_memory()
        assert result == ""

    def test_empty_files_list_returns_empty_string(self, tmp_path):
        """When academic_memory_files is empty list, return ''."""
        mw = _make_middleware(
            academic_memory_dir=str(tmp_path),
            academic_memory_category="ml",
            academic_memory_files=[],
        )
        result = mw._read_academic_memory()
        assert result == ""

    def test_path_traversal_rejected(self, tmp_path):
        """Filenames containing / or .. must be rejected with ValueError."""
        mw = _make_middleware(
            academic_memory_dir=str(tmp_path),
            academic_memory_category="ml",
            academic_memory_files=["../secret.txt"],
        )
        with pytest.raises(ValueError, match="Invalid academic memory filename"):
            mw._read_academic_memory()

    def test_path_with_slash_rejected(self, tmp_path):
        """Filenames containing / are rejected."""
        mw = _make_middleware(
            academic_memory_dir=str(tmp_path),
            academic_memory_category="ml",
            academic_memory_files=["subdir/TASTE.md"],
        )
        with pytest.raises(ValueError, match="Invalid academic memory filename"):
            mw._read_academic_memory()

    def test_no_category_uses_dir_directly(self, tmp_path):
        """When category is None, files are read directly from academic_memory_dir."""
        (tmp_path / "METHODOLOGY.md").write_text("methodology content")

        mw = _make_middleware(
            academic_memory_dir=str(tmp_path),
            academic_memory_category=None,
            academic_memory_files=["METHODOLOGY.md"],
        )
        result = mw._read_academic_memory()
        assert "methodology content" in result


# ---------------------------------------------------------------------------
# Tests for modify_request with academic memory
# ---------------------------------------------------------------------------


class TestModifyRequestAcademicMemory:
    """Tests for academic memory injection in modify_request."""

    def test_backward_compatible_no_academic_config(self):
        """Without academic_memory_dir, modify_request behaves exactly as before."""
        mw = _make_middleware(academic_memory_dir=None)
        request = _make_request()

        with patch(
            "deepagents.middleware._utils.append_to_system_message",
            side_effect=lambda sys, inj: (sys or "") + inj,
        ):
            result = mw.modify_request(request)

        # No <academic_memory> should appear
        assert "<academic_memory>" not in result.system_message

    def test_academic_memory_injected_when_configured(self, tmp_path):
        """When configured and files exist, system prompt contains <academic_memory>."""
        category_dir = tmp_path / "cv"
        category_dir.mkdir()
        (category_dir / "WRITER.md").write_text("Write like a Nature paper.")

        mw = _make_middleware(
            academic_memory_dir=str(tmp_path),
            academic_memory_category="cv",
            academic_memory_files=["WRITER.md"],
        )
        request = _make_request()

        with patch(
            "deepagents.middleware._utils.append_to_system_message",
            side_effect=lambda sys, inj: (sys or "") + inj,
        ):
            result = mw.modify_request(request)

        assert "<academic_memory>" in result.system_message
        assert "Write like a Nature paper." in result.system_message

    def test_academic_memory_appended_after_evo_memory(self, tmp_path):
        """<academic_memory> block appears after the <evo_memory> injection."""
        category_dir = tmp_path / "cat"
        category_dir.mkdir()
        (category_dir / "TASTE.md").write_text("taste data")

        mw = _make_middleware(
            academic_memory_dir=str(tmp_path),
            academic_memory_category="cat",
            academic_memory_files=["TASTE.md"],
        )
        request = _make_request()

        injections = []

        def _capture_append(sys_msg, injection):
            injections.append(injection)
            return (sys_msg or "") + injection

        with patch(
            "deepagents.middleware._utils.append_to_system_message",
            side_effect=_capture_append,
        ):
            mw.modify_request(request)

        # First injection: evo_memory; second: academic_memory
        assert len(injections) == 2
        assert "<evo_memory>" in injections[0]
        assert "<academic_memory>" in injections[1]
