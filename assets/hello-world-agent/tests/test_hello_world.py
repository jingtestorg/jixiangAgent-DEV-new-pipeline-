"""Unit and integration tests for the Hello World Agent."""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add app/ to path so we can import agent modules (conftest also does this via add_agent_to_path,
# but we add it here explicitly so the test file is self-contained for collection)
APP_PATH = str(Path(__file__).parent.parent / "app")
if APP_PATH not in sys.path:
    sys.path.insert(0, APP_PATH)

# Ensure mcp_tools module is importable before patching
import importlib
import mcp_tools  # noqa: F401


# ---------------------------------------------------------------------------
# Unit test: hello world response
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_agent_responds_hello_world():
    """Agent must respond with 'hello world' for any input."""
    with patch("mcp_tools.get_mcp_tools", new_callable=AsyncMock, return_value=[]):
        from agent import SampleAgent

        agent = SampleAgent()

        # Mock the LLM to return "hello world"
        mock_llm_response = MagicMock()
        mock_llm_response.content = "hello world"

        with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = {"messages": [mock_llm_response]}

            chunks = []
            async for chunk in agent.stream("hi there", "test-ctx-001"):
                chunks.append(chunk)

            final = chunks[-1]
            assert final["is_task_complete"] is True
            assert "hello world" in final["content"].lower()


@pytest.mark.asyncio
async def test_agent_responds_hello_world_any_message():
    """Agent must respond with 'hello world' regardless of input message."""
    with patch("mcp_tools.get_mcp_tools", new_callable=AsyncMock, return_value=[]):
        from agent import SampleAgent

        agent = SampleAgent()

        mock_llm_response = MagicMock()
        mock_llm_response.content = "hello world"

        with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = {"messages": [mock_llm_response]}

            result = await agent.invoke("tell me something random", "test-ctx-002")

            assert result.status == "completed"
            assert "hello world" in result.message.lower()


# ---------------------------------------------------------------------------
# Integration test: end-to-end agent flow
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_agent_invoke_end_to_end():
    """Integration test: invoke agent end-to-end with mocked LLM."""
    with patch("mcp_tools.get_mcp_tools", new_callable=AsyncMock, return_value=[]):
        from agent import SampleAgent

        agent = SampleAgent()

        mock_llm_response = MagicMock()
        mock_llm_response.content = "hello world"

        with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = {"messages": [mock_llm_response]}

            result = await agent.invoke("Hello!", "integration-test-ctx")

            assert result.status == "completed"
            assert result.message == "hello world"
            mock_invoke.assert_called_once()


@pytest.mark.asyncio
async def test_agent_handles_error_gracefully():
    """Agent must handle exceptions without crashing — returns a graceful message."""
    with patch("mcp_tools.get_mcp_tools", new_callable=AsyncMock, return_value=[]):
        from agent import SampleAgent

        agent = SampleAgent()

        with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.side_effect = RuntimeError("LLM unavailable")

            result = await agent.invoke("any message", "error-test-ctx")

            # Framework returns completed status with a graceful error message
            assert result.status == "completed"
            assert result.message is not None
            assert len(result.message) > 0


# ---------------------------------------------------------------------------
# System prompt test
# ---------------------------------------------------------------------------


def test_system_prompt_contains_hello_world():
    """System prompt must instruct the agent to respond with 'hello world'."""
    from agent import get_system_prompt

    prompt = get_system_prompt()
    assert "hello world" in prompt.lower()
