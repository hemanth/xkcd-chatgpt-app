"""MCP request handlers for XKCD widget following OpenAI patterns."""

from typing import Any, Dict

import mcp.types as types
from pydantic import ValidationError

from .html_generator import generate_comic_html, generate_error_html
from .models import AppWidget, ToolInput
from .widgets import get_widget_by_id, get_widget_by_uri
from .xkcd_client import extract_comic_number, fetch_xkcd_comic


# Cache to store the latest widget HTML (updated after each tool call)
WIDGET_HTML_CACHE: Dict[str, str] = {}


def get_tool_meta(widget: AppWidget) -> Dict[str, Any]:
    """Generate OpenAI-specific metadata for widgets.

    Args:
        widget: The widget to generate metadata for

    Returns:
        Metadata dictionary
    """
    return {
        "openai/outputTemplate": widget.template_uri,
        "openai/toolInvocation/invoking": widget.invoking,
        "openai/toolInvocation/invoked": widget.invoked,
        "openai/widgetAccessible": True,
        "openai/resultCanProduceWidget": True,
        "annotations": {
            "destructiveHint": False,
            "openWorldHint": False,
            "readOnlyHint": True,
        }
    }


def create_embedded_resource(widget: AppWidget, mime_type: str) -> types.EmbeddedResource:
    """Create an embedded widget resource.

    Args:
        widget: The widget to embed
        mime_type: MIME type for the resource

    Returns:
        Embedded resource
    """
    return types.EmbeddedResource(
        type="resource",
        resource=types.TextResourceContents(
            uri=widget.template_uri,
            mimeType=mime_type,
            text=widget.html,
            title=widget.title,
        ),
    )


async def handle_read_resource(
    req: types.ReadResourceRequest,
    mime_type: str
) -> types.ServerResult:
    """Handle read resource requests.

    Args:
        req: The read resource request
        mime_type: MIME type for resources

    Returns:
        Server result with resource contents
    """
    widget = get_widget_by_uri(str(req.params.uri))
    if widget is None:
        return types.ServerResult(
            types.ReadResourceResult(
                contents=[],
                _meta={"error": f"Unknown resource: {req.params.uri}"},
            )
        )

    # Use cached HTML if available (updated after tool calls), otherwise use the default template
    html_content = WIDGET_HTML_CACHE.get(widget.template_uri, widget.html)

    contents = [
        types.TextResourceContents(
            uri=widget.template_uri,
            mimeType=mime_type,
            text=html_content,
            _meta=get_tool_meta(widget),
        )
    ]

    return types.ServerResult(types.ReadResourceResult(contents=contents))


async def handle_call_tool(
    req: types.CallToolRequest,
    mime_type: str
) -> types.ServerResult:
    """Handle tool call requests.

    Args:
        req: The tool call request
        mime_type: MIME type for resources

    Returns:
        Server result with tool execution results
    """
    widget = get_widget_by_id(req.params.name)
    if widget is None:
        return types.ServerResult(
            types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Unknown tool: {req.params.name}",
                    )
                ],
                isError=True,
            )
        )

    # Validate input
    arguments = req.params.arguments or {}
    try:
        payload = ToolInput.model_validate(arguments)
    except ValidationError as exc:
        return types.ServerResult(
            types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Input validation error: {exc.errors()}",
                    )
                ],
                isError=True,
            )
        )

    # Fetch XKCD comic
    try:
        # First check if comic_number was explicitly provided
        comic_number = payload.comic_number

        # If not, try to extract from the user query (URL or number)
        if comic_number is None:
            comic_number = extract_comic_number(payload.user_query)

        comic_data = await fetch_xkcd_comic(comic_number)

        # Generate HTML with the fetched comic
        comic_html = generate_comic_html(comic_data)

        # Cache the HTML so it's available when the resource is requested
        WIDGET_HTML_CACHE[widget.template_uri] = comic_html

        # Update widget with the new HTML
        updated_widget = AppWidget(
            identifier=widget.identifier,
            title=widget.title,
            template_uri=widget.template_uri,
            invoking=widget.invoking,
            invoked=widget.invoked,
            html=comic_html,
            response_text=f"Displaying XKCD #{comic_data['num']}: {comic_data['title']}",
        )

        result_data = {
            "comic_number": comic_data.get("num"),
            "title": comic_data.get("title"),
            "alt": comic_data.get("alt"),
            "img": comic_data.get("img"),
            "date": f"{comic_data.get('year')}-{int(comic_data.get('month', 1)):02d}-{int(comic_data.get('day', 1)):02d}",
        }

        # Build embedded widget resource with updated widget
        widget_resource = create_embedded_resource(updated_widget, mime_type)
    except Exception as e:
        # Handle errors gracefully
        error_html = generate_error_html(str(e))

        # Cache the error HTML
        WIDGET_HTML_CACHE[widget.template_uri] = error_html

        updated_widget = AppWidget(
            identifier=widget.identifier,
            title=widget.title,
            template_uri=widget.template_uri,
            invoking=widget.invoking,
            invoked=widget.invoked,
            html=error_html,
            response_text=f"Error: {str(e)}",
        )
        widget_resource = create_embedded_resource(updated_widget, mime_type)
        result_data = {"error": str(e)}

    meta: Dict[str, Any] = {
        "openai.com/widget": widget_resource.model_dump(mode="json"),
        "openai/outputTemplate": updated_widget.template_uri,
        "openai/toolInvocation/invoking": updated_widget.invoking,
        "openai/toolInvocation/invoked": updated_widget.invoked,
        "openai/widgetAccessible": True,
        "openai/resultCanProduceWidget": True,
    }

    return types.ServerResult(
        types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text=updated_widget.response_text,
                )
            ],
            structuredContent=result_data,
            _meta=meta,
        )
    )
