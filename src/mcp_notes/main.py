"""MCP Notes server main entry point."""

import asyncio
import sys
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

import sys
from pathlib import Path

# Add src to path so we can import our modules
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from mcp_notes.config.settings import get_vault_path
from mcp_notes.lib.file_manager import FileManager
from mcp_notes.lib.git import GitManager
from mcp_notes.lib.search import SearchEngine
from mcp_notes.lib.markdown import (
    create_default_frontmatter, 
    format_markdown, 
    parse_markdown,
    extract_title_from_content
)
from mcp_notes.lib.types import (
    CreateNoteParams,
    SearchNotesParams, 
    ListNotesParams,
    GetNoteParams,
    NoteFrontmatter
)


class MCPNotesServer:
    """MCP Notes server implementation."""
    
    def __init__(self, vault_path: str):
        self.file_manager = FileManager(vault_path)
        self.git_manager = GitManager(vault_path)
        self.search_engine = SearchEngine(self.file_manager)
        self.server = Server("mcp-notes")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register MCP tools."""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            return [
                Tool(
                    name="create_note",
                    description="Create a new markdown note with frontmatter and git commit",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Note title"},
                            "content": {"type": "string", "description": "Note content in markdown"},
                            "summary": {"type": "string", "description": "Brief summary of the note"},
                            "tags": {
                                "type": "array", 
                                "items": {"type": "string"},
                                "description": "Tags for categorization"
                            },
                            "conversation_id": {"type": "string", "description": "ID of related conversation"},
                            "ai_client": {"type": "string", "description": "AI client that created the note"}
                        },
                        "required": ["title", "content"]
                    }
                ),
                Tool(
                    name="search_notes",
                    description="Search existing notes with relevance scoring",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search query"},
                            "limit": {"type": "integer", "description": "Maximum results", "default": 10},
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Filter by tags"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="list_notes", 
                    description="List notes with filtering and sorting options",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {"type": "integer", "description": "Maximum results", "default": 20},
                            "offset": {"type": "integer", "description": "Results offset", "default": 0},
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Filter by tags"
                            },
                            "sort_by": {"type": "string", "description": "Sort field", "default": "created"},
                            "sort_order": {"type": "string", "description": "Sort order (asc/desc)", "default": "desc"}
                        }
                    }
                ),
                Tool(
                    name="get_note",
                    description="Retrieve complete note content by filename",
                    inputSchema={
                        "type": "object", 
                        "properties": {
                            "filename": {"type": "string", "description": "Note filename"}
                        },
                        "required": ["filename"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            if name == "create_note":
                return await self._create_note(arguments)
            elif name == "search_notes":
                return await self._search_notes(arguments)
            elif name == "list_notes":
                return await self._list_notes(arguments)
            elif name == "get_note":
                return await self._get_note(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def _create_note(self, args: Dict[str, Any]) -> List[TextContent]:
        """Create a new note."""
        try:
            params = CreateNoteParams(**args)
            
            # Generate filename
            filename = self.file_manager.generate_filename(params.title)
            
            # Check if note already exists
            if self.file_manager.note_exists(filename):
                return [TextContent(
                    type="text",
                    text=f"Error: Note with filename '{filename}' already exists"
                )]
            
            # Create frontmatter
            frontmatter = create_default_frontmatter(
                params.title,
                params.summary,
                params.tags,
                params.conversation_id,
                params.ai_client
            )
            
            # Format complete markdown
            full_content = format_markdown(frontmatter, params.content)
            
            # Write note
            self.file_manager.write_note(filename, full_content)
            
            # Commit to git
            commit_msg = f"Add note: {params.title}"
            success = self.git_manager.commit_note(filename, commit_msg)
            
            git_status = "committed to git" if success else "saved but git commit failed"
            
            return [TextContent(
                type="text",
                text=f"Note created successfully: {filename} ({git_status})"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text", 
                text=f"Error creating note: {str(e)}"
            )]
    
    async def _search_notes(self, args: Dict[str, Any]) -> List[TextContent]:
        """Search notes with relevance scoring."""
        try:
            params = SearchNotesParams(**args)
            results = self.search_engine.search_notes(
                params.query,
                params.limit or 10,
                params.tags or []
            )
            
            if not results:
                return [TextContent(
                    type="text",
                    text="No notes found matching your search."
                )]
            
            # Format results
            result_text = f"Found {len(results)} note(s):\n\n"
            for result in results:
                result_text += f"**{result.title}** (score: {result.relevance_score:.2f})\n"
                result_text += f"File: {result.filename}\n"
                result_text += f"Summary: {result.summary}\n"
                if result.tags:
                    result_text += f"Tags: {', '.join(result.tags)}\n"
                result_text += f"Created: {result.created}\n\n"
            
            return [TextContent(type="text", text=result_text)]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error searching notes: {str(e)}"
            )]
    
    async def _list_notes(self, args: Dict[str, Any]) -> List[TextContent]:
        """List notes with filtering and sorting."""
        try:
            params = ListNotesParams(**args)
            notes = self.file_manager.list_notes()
            
            # Filter and collect note metadata
            note_data = []
            for filename in notes:
                try:
                    content = self.file_manager.read_note(filename)
                    parsed = parse_markdown(content)
                    
                    # Filter by tags if specified
                    if params.tags:
                        if not any(tag in parsed.frontmatter.tags for tag in params.tags):
                            continue
                    
                    title = extract_title_from_content(content) or filename.replace('.md', '')
                    
                    note_data.append({
                        'filename': filename,
                        'title': title,
                        'summary': parsed.frontmatter.summary,
                        'tags': parsed.frontmatter.tags,
                        'created': parsed.frontmatter.created,
                        'updated': parsed.frontmatter.updated
                    })
                except Exception:
                    continue
            
            # Sort notes
            reverse = params.sort_order == "desc"
            if params.sort_by == "title":
                note_data.sort(key=lambda x: x['title'], reverse=reverse)
            elif params.sort_by == "updated":
                note_data.sort(key=lambda x: x['updated'], reverse=reverse)
            else:  # created (default)
                note_data.sort(key=lambda x: x['created'], reverse=reverse)
            
            # Apply pagination
            start = params.offset or 0
            end = start + (params.limit or 20)
            page_notes = note_data[start:end]
            
            if not page_notes:
                return [TextContent(
                    type="text",
                    text="No notes found."
                )]
            
            # Format results
            result_text = f"Found {len(note_data)} total note(s), showing {len(page_notes)}:\n\n"
            for note in page_notes:
                result_text += f"**{note['title']}**\n"
                result_text += f"File: {note['filename']}\n"
                result_text += f"Summary: {note['summary']}\n"
                if note['tags']:
                    result_text += f"Tags: {', '.join(note['tags'])}\n"
                result_text += f"Created: {note['created']}\n\n"
            
            return [TextContent(type="text", text=result_text)]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error listing notes: {str(e)}"
            )]
    
    async def _get_note(self, args: Dict[str, Any]) -> List[TextContent]:
        """Get complete note content."""
        try:
            params = GetNoteParams(**args)
            
            if not self.file_manager.note_exists(params.filename):
                return [TextContent(
                    type="text",
                    text=f"Note not found: {params.filename}"
                )]
            
            content = self.file_manager.read_note(params.filename)
            
            return [TextContent(
                type="text",
                text=f"Content of {params.filename}:\n\n{content}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error retrieving note: {str(e)}"
            )]
    
    async def run(self) -> None:
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream, self.server.create_initialization_options())


async def main():
    """Main entry point."""
    try:
        vault_path = get_vault_path()
        server = MCPNotesServer(vault_path)
        await server.run()
    except Exception as e:
        print(f"Server failed to start: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())