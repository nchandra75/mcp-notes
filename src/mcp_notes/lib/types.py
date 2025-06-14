"""Type definitions for MCP Notes."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class NoteFrontmatter(BaseModel):
    """YAML frontmatter for markdown notes."""
    created: str
    updated: str
    tags: List[str] = []
    summary: str
    conversation_id: Optional[str] = None
    ai_client: Optional[str] = None


class Note(BaseModel):
    """Complete note with frontmatter and content."""
    filename: str
    frontmatter: NoteFrontmatter
    content: str
    

class SearchResult(BaseModel):
    """Search result with relevance scoring."""
    filename: str
    title: str
    summary: str
    relevance_score: float
    tags: List[str]
    created: str


class CreateNoteParams(BaseModel):
    """Parameters for creating a new note."""
    title: str
    content: str
    summary: Optional[str] = None
    tags: Optional[List[str]] = None
    conversation_id: Optional[str] = None
    ai_client: Optional[str] = None


class SearchNotesParams(BaseModel):
    """Parameters for searching notes."""
    query: str
    limit: Optional[int] = 10
    tags: Optional[List[str]] = None


class ListNotesParams(BaseModel):
    """Parameters for listing notes."""
    limit: Optional[int] = 20
    offset: Optional[int] = 0
    tags: Optional[List[str]] = None
    sort_by: Optional[str] = "created"  # created, updated, title
    sort_order: Optional[str] = "desc"  # asc, desc


class GetNoteParams(BaseModel):
    """Parameters for getting a specific note."""
    filename: str