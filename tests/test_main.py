"""Tests for XKCD Cartoon Viewer."""

import pytest
from httpx import AsyncClient
import sys
from pathlib import Path

# Add parent directory to path to import main
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app, ToolInput


@pytest.mark.asyncio
async def test_health_check():
    """Test that the server is running."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # The MCP endpoint should be accessible
        response = await client.get("/mcp")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_tool_input_validation():
    """Test input validation for tools."""
    # Valid input
    valid_input = {"userQuery": "test query"}
    payload = ToolInput.model_validate(valid_input)
    assert payload.user_query == "test query"
    assert payload.options == {}

    # Valid input with options
    valid_input_with_options = {
        "userQuery": "test query",
        "options": {"key": "value"}
    }
    payload = ToolInput.model_validate(valid_input_with_options)
    assert payload.user_query == "test query"
    assert payload.options == {"key": "value"}

    # Invalid input - missing required field
    invalid_input = {"wrongField": "test"}
    with pytest.raises(Exception):
        ToolInput.model_validate(invalid_input)

    # Invalid input - extra fields not allowed
    invalid_extra = {
        "userQuery": "test",
        "extraField": "not allowed"
    }
    with pytest.raises(Exception):
        ToolInput.model_validate(invalid_extra)


def test_widgets_configured():
    """Test that widgets are properly configured."""
    from main import widgets, WIDGETS_BY_ID, WIDGETS_BY_URI

    # Check that widgets list is not empty
    assert len(widgets) > 0

    # Check that lookup dictionaries are populated
    assert len(WIDGETS_BY_ID) == len(widgets)
    assert len(WIDGETS_BY_URI) == len(widgets)

    # Verify each widget has required fields
    for widget in widgets:
        assert widget.identifier
        assert widget.title
        assert widget.template_uri
        assert widget.html
        assert widget.response_text

    # Test specific widgets
    assert "xkcd-viewer" in WIDGETS_BY_ID
    assert "ui://widget/xkcd-viewer.html" in WIDGETS_BY_URI


def test_mime_type():
    """Test that MIME type is correctly set."""
    from main import MIME_TYPE
    assert MIME_TYPE == "text/html+skybridge"


def test_tool_input_schema():
    """Test that tool input schema is valid."""
    from main import TOOL_INPUT_SCHEMA

    assert TOOL_INPUT_SCHEMA["type"] == "object"
    assert "userQuery" in TOOL_INPUT_SCHEMA["properties"]
    assert "userQuery" in TOOL_INPUT_SCHEMA["required"]
    assert TOOL_INPUT_SCHEMA["additionalProperties"] is False