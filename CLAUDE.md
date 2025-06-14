# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server that enables AI assistants to create, search, and manage conversation summaries as markdown notes in Obsidian vaults. The project uses Deno/TypeScript and integrates with Claude Desktop via stdio/JSON-RPC.

## Development Commands

```bash
# Initialize Deno project
deno init

# Run the MCP server
deno run --allow-read --allow-write --allow-run --allow-env src/main.ts

# Check TypeScript
deno check src/main.ts

# Format code
deno fmt

# Lint code
deno lint
```

## Architecture

The MCP server acts as a bridge between AI clients and Obsidian vaults:

- **Protocol**: JSON-RPC over stdio
- **Runtime**: Deno with TypeScript
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
src/
├── main.ts              # MCP server entry point
├── tools/               # MCP tool implementations
│   ├── create_note.ts
│   ├── search_notes.ts
│   ├── list_notes.ts
│   └── get_note.ts
├── lib/                 # Core utilities
│   ├── file_manager.ts  # File system operations
│   ├── markdown.ts      # Markdown formatting
│   ├── search.ts        # Search functionality
│   ├── git.ts           # Git operations
│   └── types.ts         # TypeScript interfaces
└── config/
    └── settings.ts      # Configuration management
```

## Note Format

Notes use markdown with YAML frontmatter:

- **Naming**: kebab-case filenames (e.g., `python-async-patterns-2025-06-14.md`)
- **Frontmatter**: created, updated, conversation_id, tags, ai_client, summary
- **Structure**: Title, Key Learnings, Code Snippets, Follow-up Questions, References

## Environment Configuration

- `OBSIDIAN_VAULT_PATH` - Path to Obsidian vault directory
- `GIT_COMMIT_TEMPLATE` - Custom commit message template (optional)

## Key Implementation Notes

- File operations must be safe (kebab-case naming, no spaces)
- All note creation should include git commits
- Search functionality requires full-text indexing across note content
- TypeScript interfaces should match the frontmatter schema exactly
- Error handling is critical for file system and git operations

## MCP Server Configuration for Claude Code

To test the MCP server with Claude Code, use these commands:

```bash
# Test the MCP server (requires OBSIDIAN_VAULT_PATH environment variable)
OBSIDIAN_VAULT_PATH="/path/to/test/vault" deno run --allow-read --allow-write --allow-run --allow-env src/main.ts

# Test with a temporary vault for safe testing
mkdir -p /tmp/test-vault
cd /tmp/test-vault && git init
OBSIDIAN_VAULT_PATH="/tmp/test-vault" deno run --allow-read --allow-write --allow-run --allow-env /home/nitin/scratch/mcp-notes/src/main.ts
```

## Available MCP Tools

1. **create_note** - Create new markdown notes with frontmatter
2. **search_notes** - Search existing notes with relevance scoring  
3. **list_notes** - Browse and filter notes with sorting options
4. **get_note** - Retrieve complete note content by filename
