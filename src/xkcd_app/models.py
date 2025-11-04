"""Data models for the XKCD ChatGPT App."""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


@dataclass(frozen=True)
class AppWidget:
    """Widget data structure for XKCD ChatGPT App."""
    identifier: str
    title: str
    template_uri: str
    invoking: str
    invoked: str
    html: str
    response_text: str


class ToolInput(BaseModel):
    """Schema for tool inputs."""

    user_query: str = Field(
        ...,
        alias="userQuery",
        description="The user's request (e.g., 'show me latest', 'https://xkcd.com/327/', 'show comic 2000', '#327')",
    )

    comic_number: Optional[int] = Field(
        None,
        alias="comicNumber",
        description="Specific XKCD comic number to fetch (optional)",
    )

    options: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional parameters",
    )

    model_config = ConfigDict(populate_by_name=True, extra="forbid")
