"""XKCD ChatGPT App - MCP Server following OpenAI Apps SDK patterns.

This server exposes widget-backed tools that render XKCD comics. Each handler returns
HTML via an MCP resource and structured comic data so the ChatGPT client can hydrate
the widget properly.
"""

from copy import deepcopy
from typing import Any, Dict, List

import mcp.types as types
from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route

from src.xkcd_app import ALL_WIDGETS, get_tool_meta, handle_call_tool, handle_read_resource


# Constants
MIME_TYPE = "text/html+skybridge"

# Tool input schema for MCP protocol
TOOL_INPUT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "userQuery": {
            "type": "string",
            "description": (
                "The user's request - can be a URL, comic number, or natural language "
                "(e.g., 'https://xkcd.com/327/', 'show comic 2000', '#327', 'show me latest')"
            ),
        },
        "comicNumber": {
            "type": "integer",
            "description": "Specific XKCD comic number to fetch (optional)",
        },
        "options": {
            "type": "object",
            "description": "Optional parameters",
        }
    },
    "required": ["userQuery"],
    "additionalProperties": False,
}


# Initialize FastMCP server
mcp = FastMCP(
    name="XKCD ChatGPT App",
    sse_path="/mcp",
    message_path="/mcp/messages",
    stateless_http=True,
    dependencies=[],
)


@mcp._mcp_server.list_tools()
async def list_tools() -> List[types.Tool]:
    """Register all available tools.

    Returns a tool definition for each widget in the server's widget registry.
    """
    return [
        types.Tool(
            name=widget.identifier,
            title=widget.title,
            description=widget.title,
            inputSchema=deepcopy(TOOL_INPUT_SCHEMA),
            _meta=get_tool_meta(widget),
        )
        for widget in ALL_WIDGETS
    ]


@mcp._mcp_server.list_resources()
async def list_resources() -> List[types.Resource]:
    """Expose widgets as resources.

    Returns a resource for each widget's HTML template.
    """
    return [
        types.Resource(
            name=widget.title,
            title=widget.title,
            uri=widget.template_uri,
            description=f"{widget.title} widget markup",
            mimeType=MIME_TYPE,
            _meta=get_tool_meta(widget),
        )
        for widget in ALL_WIDGETS
    ]


@mcp._mcp_server.list_resource_templates()
async def list_resource_templates() -> List[types.ResourceTemplate]:
    """Define resource templates.

    Returns a resource template for each widget type.
    """
    return [
        types.ResourceTemplate(
            name=widget.title,
            title=widget.title,
            uriTemplate=widget.template_uri,
            description=f"{widget.title} widget markup",
            mimeType=MIME_TYPE,
            _meta=get_tool_meta(widget),
        )
        for widget in ALL_WIDGETS
    ]


# Register request handlers
mcp._mcp_server.request_handlers[types.CallToolRequest] = lambda req: handle_call_tool(
    req, MIME_TYPE
)
mcp._mcp_server.request_handlers[types.ReadResourceRequest] = lambda req: handle_read_resource(
    req, MIME_TYPE
)


# Create FastAPI app
app = mcp.streamable_http_app()

# Add CORS middleware for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)


# Health check endpoints
async def root_handler(request):
    """Public health check endpoint - No authentication required."""
    return JSONResponse({
        "name": "XKCD ChatGPT App",
        "status": "running",
        "version": "1.0.0",
        "widgets": len(ALL_WIDGETS),
        "endpoints": {
            "mcp": "/mcp",
            "messages": "/mcp/messages",
            "health": "/health",
        },
        "description": "MCP server for fetching and displaying XKCD comics",
        "auth_required": False,
    })


async def health_handler(request):
    """Health check endpoint - No authentication required."""
    return JSONResponse({
        "status": "healthy",
        "auth_required": False,
        "widgets_count": len(ALL_WIDGETS),
    })


# Add routes
app.routes.insert(0, Route("/", root_handler))
app.routes.insert(1, Route("/health", health_handler))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
