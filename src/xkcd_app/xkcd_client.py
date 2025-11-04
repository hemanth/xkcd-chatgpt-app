"""XKCD API client for fetching comics."""

import base64
import re
from typing import Any, Dict, Optional

import httpx


def extract_comic_number(text: str) -> Optional[int]:
    """Extract XKCD comic number from URL or text.

    Supports formats:
    - https://xkcd.com/327/
    - https://xkcd.com/327
    - http://xkcd.com/327/
    - xkcd.com/327
    - Plain numbers: 327, #327

    Args:
        text: User input text that might contain a URL or comic number

    Returns:
        Comic number if found, None otherwise
    """
    url_patterns = [
        r'xkcd\.com/(\d+)',  # Matches xkcd.com/327 or https://xkcd.com/327/
        r'#(\d+)',           # Matches #327
        r'\b(\d+)\b',        # Matches standalone numbers like 327
    ]

    for pattern in url_patterns:
        match = re.search(pattern, text)
        if match:
            try:
                return int(match.group(1))
            except (ValueError, IndexError):
                continue

    return None


async def fetch_xkcd_comic(comic_number: Optional[int] = None) -> Dict[str, Any]:
    """Fetch XKCD comic data from the API.

    Args:
        comic_number: Specific comic number, or None for the latest comic

    Returns:
        Dictionary containing comic data with base64 encoded image
    """
    async with httpx.AsyncClient() as client:
        if comic_number is None:
            url = "https://xkcd.com/info.0.json"
        else:
            url = f"https://xkcd.com/{comic_number}/info.0.json"

        response = await client.get(url)
        response.raise_for_status()
        comic_data = response.json()

        # Fetch the image and convert to base64 to bypass CSP restrictions
        img_url = comic_data.get('img', '')
        if img_url:
            try:
                img_response = await client.get(img_url)
                img_response.raise_for_status()
                img_base64 = base64.b64encode(img_response.content).decode('utf-8')

                # Determine image type from URL
                if img_url.endswith('.png'):
                    mime_type = 'image/png'
                elif img_url.endswith('.jpg') or img_url.endswith('.jpeg'):
                    mime_type = 'image/jpeg'
                elif img_url.endswith('.gif'):
                    mime_type = 'image/gif'
                else:
                    mime_type = 'image/png'

                comic_data['img_base64'] = f"data:{mime_type};base64,{img_base64}"
                comic_data['img_original'] = img_url
            except Exception:
                # If image fetch fails, keep the original URL
                comic_data['img_base64'] = img_url
                comic_data['img_original'] = img_url

        return comic_data
