"""Widget definitions for XKCD ChatGPT App following OpenAI patterns."""

from typing import Dict, List

from .html_generator import PLACEHOLDER_HTML
from .models import AppWidget


# Define all available widgets
XKCD_VIEWER_WIDGET = AppWidget(
    identifier="xkcd-viewer",
    title="XKCD Comic Viewer",
    template_uri="ui://widget/xkcd-viewer.html",
    invoking="Fetching XKCD comic...",
    invoked="XKCD comic loaded successfully",
    html=PLACEHOLDER_HTML,
    response_text="Ready to fetch XKCD comics. Request a comic to get started!",
)

# List of all widgets (extensible for adding more widgets)
ALL_WIDGETS: List[AppWidget] = [
    XKCD_VIEWER_WIDGET,
]

# Build lookup dictionaries for efficient access
WIDGETS_BY_ID: Dict[str, AppWidget] = {
    widget.identifier: widget for widget in ALL_WIDGETS
}

WIDGETS_BY_URI: Dict[str, AppWidget] = {
    widget.template_uri: widget for widget in ALL_WIDGETS
}


def get_widget_by_id(identifier: str) -> AppWidget | None:
    """Get widget by identifier.

    Args:
        identifier: Widget identifier

    Returns:
        Widget if found, None otherwise
    """
    return WIDGETS_BY_ID.get(identifier)


def get_widget_by_uri(uri: str) -> AppWidget | None:
    """Get widget by template URI.

    Args:
        uri: Widget template URI

    Returns:
        Widget if found, None otherwise
    """
    return WIDGETS_BY_URI.get(uri)
