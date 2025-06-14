# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server that enables AI assistants to create, search, and manage conversation summaries as markdown notes in Obsidian vaults. The project uses Python with uv for dependency management and integrates with Claude Desktop via stdio/JSON-RPC.

## Development Commands

```bash
# Initialize Python project with uv
uv init --name mcp-notes --python 3.11

# Install dependencies
uv add mcp pydantic pyyaml gitpython

# Run the MCP server
cd /path/to/mcp-notes && OBSIDIAN_VAULT_PATH="/path/to/vault" uv run src/mcp_notes/main.py

# Format code
uv run ruff format

# Lint code  
uv run ruff check

# Type check
uv run mypy src/mcp_notes

# Run tests
uv run pytest tests/ -v
```

## Architecture

The MCP server acts as a bridge between AI clients and Obsidian vaults:

- **Protocol**: JSON-RPC over stdio
- **Runtime**: Python 3.11+ with uv dependency management
- **Storage**: Markdown files with YAML frontmatter
- **Integration**: Direct file system access to Obsidian vault
- **Version Control**: Git commits for each note creation

## Core MCP Tools to Implement

1. **create_note** - Create structured markdown notes with git commits
2. **search_notes** - Full-text search with relevance scoring
3. **list_notes** - Browse notes with filtering options
4. **get_note** - Retrieve specific note content
5. **suggest_note** - AI-driven note creation suggestions

## Project Structure

```
src/mcp_notes/
├── main.py              # MCP server entry point
├── lib/                 # Core utilities
│   ├── __init__.py
│   ├── file_manager.py  # File system operations
│   ├── markdown.py      # Markdown formatting
│   ├── search.py        # Search functionality
│   ├── git.py           # Git operations
│   └── types.py         # Pydantic models and types
├── tools/               # MCP tool implementations (integrated in main.py)
│   └── __init__.py
└── config/
    ├── __init__.py
    └── settings.py      # Configuration management
```

## Note Format

Notes use markdown with YAML frontmatter:

- **Naming**: kebab-case filenames (e.g., `python-async-patterns-2025-06-14.md`)
- **Frontmatter**: created, updated, conversation_id, tags, ai_client, summary
- **Structure**: Title, Key Learnings, Code Snippets, Follow-up Questions, References
- **Date Backlink**: Automatically appends `Created: [[YYYY-MM-DD]]` for Obsidian navigation

## Environment Configuration

- `OBSIDIAN_VAULT_PATH` - Path to Obsidian vault directory
- `GIT_COMMIT_TEMPLATE` - Custom commit message template (optional)

## Key Implementation Notes

- File operations must be safe (kebab-case naming, no spaces)
- All note creation should include git commits
- Search functionality requires full-text indexing across note content
- Pydantic models should match the frontmatter schema exactly
- Error handling is critical for file system and git operations

## MCP Server Configuration for Claude Code

To test the MCP server with Claude Code, use these commands:

```bash
# Test the MCP server (requires OBSIDIAN_VAULT_PATH environment variable)
cd /path/to/mcp-notes && OBSIDIAN_VAULT_PATH="/path/to/test/vault" uv run src/mcp_notes/main.py

# Test with a temporary vault for safe testing
mkdir -p ./tmp/test-vault
cd ./tmp/test-vault && git init
cd /home/nitin/scratch/mcp-notes && OBSIDIAN_VAULT_PATH="./tmp/test-vault" uv run src/mcp_notes/main.py
```

## Available MCP Tools

1. **create_note** - Create new markdown notes with frontmatter
2. **search_notes** - Search existing notes with relevance scoring  
3. **list_notes** - Browse and filter notes with sorting options
4. **get_note** - Retrieve complete note content by filename

## Testing Notes

- For tests, use "./tmp" instead of "/tmp" as you don't have direct access to /tmp. Clean up after the test.