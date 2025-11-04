"""XKCD ChatGPT App - A MCP server for displaying XKCD comics."""

__version__ = "1.0.0"
__author__ = "XKCD ChatGPT App Team"
__description__ = "MCP server for fetching and displaying XKCD comics"

from .models import AppWidget, ToolInput
from .widgets import ALL_WIDGETS, get_widget_by_id, get_widget_by_uri
from .handlers import handle_call_tool, handle_read_resource, get_tool_meta
from .html_generator import generate_comic_html, generate_error_html, PLACEHOLDER_HTML
from .xkcd_client import fetch_xkcd_comic, extract_comic_number

__all__ = [
    # Models
    "AppWidget",
    "ToolInput",
    # Widgets
    "ALL_WIDGETS",
    "get_widget_by_id",
    "get_widget_by_uri",
    # Handlers
    "handle_call_tool",
    "handle_read_resource",
    "get_tool_meta",
    # HTML Generation
    "generate_comic_html",
    "generate_error_html",
    "PLACEHOLDER_HTML",
    # XKCD Client
    "fetch_xkcd_comic",
    "extract_comic_number",
]
