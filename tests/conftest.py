"""Shared fixtures: isolate global tool state, caches, HOME, and config dirs."""

from __future__ import annotations

import pytest

from nano_claude_code.agents import clear_agent_cache
from nano_claude_code.skills import clear_skill_cache
from nano_claude_code.tools_impl import reset_transient_tool_state


@pytest.fixture(autouse=True)
def _isolate_tool_globals(tmp_path, monkeypatch):
    reset_transient_tool_state()
    clear_skill_cache()
    clear_agent_cache()

    uh = tmp_path / "user_home"
    uh.mkdir()
    monkeypatch.setenv("HOME", str(uh))

    nc = tmp_path / ".nano_claude"
    sess = nc / "sessions"
    sess.mkdir(parents=True)
    monkeypatch.setattr("nano_claude_code.config.CONFIG_DIR", nc)
    monkeypatch.setattr("nano_claude_code.config.SESSIONS_DIR", sess)
    monkeypatch.setattr("nano_claude_code.config.CONFIG_FILE", nc / "config.json")
    monkeypatch.setattr("nano_claude_code.skills.CONFIG_DIR", nc)
    monkeypatch.setattr("nano_claude_code.agents.CONFIG_DIR", nc)
    monkeypatch.setattr("nano_claude_code.session.SESSIONS_DIR", sess)

    yield

    reset_transient_tool_state()
    clear_skill_cache()
    clear_agent_cache()


@pytest.fixture
def tmp_project(tmp_path):
    """Empty git-less directory for filesystem tools."""
    return tmp_path
