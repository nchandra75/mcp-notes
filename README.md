# MCP Notes

A Model Context Protocol (MCP) server for creating, searching, and managing conversation summaries as markdown notes in Obsidian vaults.

## Overview

This MCP server enables AI assistants to automatically create structured notes from conversations, code snippets, and learnings. It integrates seamlessly with Claude Desktop and other MCP-compatible AI clients.

## Key Features

- **=Ý Note Creation**: Create structured markdown notes with YAML frontmatter
- **= Smart Search**: Full-text search with relevance scoring and tag filtering  
- **=Å Date Flexibility**: Support for custom dates like "yesterday" or "last friday"
- **= Obsidian Integration**: Automatic date backlinks for easy navigation
- **<¯ Git Tracking**: Automatic git commits for version control
- **<÷ Tag Management**: Organize notes with custom tags

## Quick Start

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Configure Claude Desktop** with your vault path:
   ```json
   {
     "mcpServers": {
       "obsidian-notes": {
         "command": "uv",
         "args": ["run", "--directory", "/path/to/mcp-notes", "src/mcp_notes/main.py"],
         "env": {
           "OBSIDIAN_VAULT_PATH": "/path/to/your/obsidian/vault"
         }
       }
     }
   }
   ```

3. **Start using**: Ask Claude to create notes from your conversations!

## Available Tools

- `create_note` - Create new markdown notes with frontmatter
- `search_notes` - Search existing notes with relevance scoring
- `list_notes` - Browse and filter your note collection  
- `get_note` - Retrieve specific note content

## Testing

Run the comprehensive test suite:

```bash
uv run pytest tests/ -v
```

## Documentation

For detailed setup instructions, API documentation, and troubleshooting:

- **[Setup Guide](docs/SETUP.md)** - Installation and configuration
- **[API Documentation](docs/API.md)** - Detailed tool reference
- **[Claude Desktop Integration](docs/CLAUDE_DESKTOP.md)** - Platform-specific setup

## Requirements

- Python 3.11+
- uv (for dependency management)
- Git (for version control)
- Obsidian (for note management)

## License

See project files for license information.