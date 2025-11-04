"""HTML generation for XKCD widget displays."""

import html
from typing import Any, Dict


PLACEHOLDER_HTML = (
    "<div style='max-width: 800px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif;'>"
    "  <div style='background: white; border: 2px solid black; border-radius: 8px; "
    "              padding: 40px; text-align: center;'>"
    "    <h1 style='color: black; margin: 0 0 20px 0; font-size: 32px; font-weight: bold;'>XKCD Comic Viewer</h1>"
    "    <div style='background: white; border: 2px dashed #333; border-radius: 4px; padding: 30px; margin: 20px 0;'>"
    "      <p style='color: black; font-size: 18px; margin: 0 0 15px 0; font-weight: bold;'>"
    "        Ready to display XKCD comics!"
    "      </p>"
    "      <p style='color: #333; font-size: 14px; margin: 0; line-height: 1.6;'>"
    "        Request a comic to see it displayed here.<br>"
    "        Try: 'Show me the latest XKCD', 'https://xkcd.com/327/', or '#327'"
    "      </p>"
    "    </div>"
    "    <div style='margin-top: 30px; padding-top: 20px; border-top: 2px solid black;'>"
    "      <p style='color: #666; margin: 0; font-size: 12px;'>"
    "        Comics by Randall Munroe • Powered by XKCD API"
    "      </p>"
    "    </div>"
    "  </div>"
    "</div>"
)


def generate_comic_html(comic_data: Dict[str, Any]) -> str:
    """Generate HTML for displaying XKCD comic.

    Args:
        comic_data: Comic data from XKCD API

    Returns:
        HTML string with embedded comic
    """
    # Escape HTML to prevent injection and attribute breaking
    title = html.escape(comic_data.get('title', 'XKCD Comic'))
    alt_text = html.escape(comic_data.get('alt', 'No alt text available'))

    # Use base64 encoded image if available, otherwise fall back to URL
    img_url = comic_data.get('img_base64', comic_data.get('img', ''))
    img_original_url = comic_data.get('img_original', comic_data.get('img', ''))

    comic_num = comic_data.get('num')
    year = comic_data.get('year')

    # XKCD API returns month and day as strings, convert to int
    month = int(comic_data.get('month', 1))
    day = int(comic_data.get('day', 1))

    return f"""
    <div style="max-width: 800px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif;">
        <div style="background: white; border: 2px solid black; border-radius: 8px; padding: 30px;">
            <h1 style="color: black; margin: 0 0 10px 0; font-size: 28px; font-weight: bold;">
                #{comic_num} - {title}
            </h1>
            <p style="color: #333; margin: 0 0 20px 0; font-size: 14px;">
                Published: {year}-{month:02d}-{day:02d}
            </p>

            <div style="background: #f5f5f5; border: 1px solid #ddd; border-radius: 4px; padding: 20px; margin-bottom: 20px; text-align: center;">
                <img src="{img_url}"
                     alt="{alt_text}"
                     title="{alt_text}"
                     style="max-width: 100%; height: auto; display: block; margin: 0 auto; border: 1px solid #ccc;"
                     loading="eager"
                     onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                <div style="display: none; padding: 20px; color: #ff4444;">
                    Failed to load image. <a href="{img_original_url}" target="_blank" style="color: #ff4444;">View original</a>
                </div>
            </div>

            <div style="background: #f9f9f9; border-left: 4px solid black; border-radius: 4px; padding: 15px; margin-bottom: 20px;">
                <p style="color: #333; margin: 0; font-size: 14px; line-height: 1.6;">
                    <strong style="color: black;">Alt text:</strong> {alt_text}
                </p>
            </div>

            <div style="margin-top: 20px; padding-top: 20px; border-top: 2px solid black; text-align: center;">
                <p style="color: #666; margin: 0; font-size: 12px;">
                    Comic by Randall Munroe • <a href="https://xkcd.com/{comic_num}"
                    target="_blank" style="color: black; text-decoration: underline;">View on xkcd.com</a>
                </p>
            </div>
        </div>
    </div>
    """


def generate_error_html(error_message: str) -> str:
    """Generate error HTML.

    Args:
        error_message: Error message to display

    Returns:
        HTML string with error message
    """
    return f"""
    <div style="padding: 20px; border: 2px solid #ff4444; border-radius: 8px; background: #fff0f0;">
        <h2 style="color: #ff4444; margin-top: 0;">Error Fetching Comic</h2>
        <p style="color: #333;">{html.escape(error_message)}</p>
    </div>
    """
