"""This module defines the Pydantic models for the submissions documents"""

from typing import Any

from pydantic import BaseModel


class Metadata(BaseModel):
    id: int | None = None
    title: str | None = None
    description: str | None = None
    author: list[str] | None = None
    document_type: str | None = None
    draft_category: list[str] | None = None
    href: str | None = None
    session: str = "5.2"
    verified: bool = False
    retriever_id: str | None = None
    key_element: dict[str, Any] | None = None
