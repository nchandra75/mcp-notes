# Obsidian Notes MCP Server

A Model Context Protocol (MCP) server that enables AI assistants to create, search, and manage conversation summaries as markdown notes in your Obsidian vault.

## Project Overview

This MCP server bridges the gap between AI conversations and personal knowledge management by automatically creating structured notes from conversation summaries, code snippets, and learnings. It integrates seamlessly with Claude Desktop and other MCP-compatible AI clients.

### Key Features

- **Conversation Summarization**: Create structured markdown notes from AI conversations
- **Code Snippet Extraction**: Automatically format and preserve code examples
- **Knowledge Search**: Find relevant past conversations and learnings
- **Obsidian Integration**: Direct file system integration with Obsidian vaults
- **Cross-Platform**: Works with any MCP-compatible AI client

## Technical Requirements

### Core Technologies

- **Runtime**: Deno (no Node.js/npm required)
- **Language**: TypeScript
- **Protocol**: Model Context Protocol (MCP)
- **File Format**: Markdown with YAML frontmatter
- **Integration**: Obsidian vault (file system based)
- **Version Control**: Git integration for automatic commits

### System Requirements

- Deno runtime installed
- Read/write access to Obsidian vault directory
- Git repository initialized in vault (optional but recommended)
- MCP-compatible AI client (Claude Desktop, Continue.dev, etc.)

## Architecture

```
AI Client (Claude Desktop) ←→ MCP Server ←→ Obsidian Vault
        (stdio/JSON-RPC)         (Deno/TS)    (Markdown files)
```

### MCP Tools to Implement

1. **`create_note`** - Create new conversation summary with git commit
   - Input: title, content, tags, conversation_id
   - Output: file path, git commit hash, success status

2. **`search_notes`** - Search existing notes
   - Input: query string, optional filters
   - Output: matching notes with relevance scores

3. **`list_notes`** - Browse note collection
   - Input: sort order, date range, tag filters
   - Output: note metadata list

4. **`get_note`** - Retrieve specific note content
   - Input: note identifier or path
   - Output: full note content and metadata

5. **`suggest_note`** - AI-driven note creation suggestion
   - Input: conversation context
   - Output: suggested title, content, tags

## File Structure

```
obsidian-notes-mcp/
├── README.md
├── deno.json                 # Deno configuration
├── src/
│   ├── main.ts              # MCP server entry point
│   ├── tools/               # MCP tool implementations
│   │   ├── create_note.ts
│   │   ├── search_notes.ts
│   │   ├── list_notes.ts
│   │   └── get_note.ts
│   ├── lib/                 # Core utilities
│   │   ├── file_manager.ts  # File system operations
│   │   ├── markdown.ts      # Markdown formatting
│   │   ├── search.ts        # Search functionality
│   │   ├── git.ts           # Git operations
│   │   └── types.ts         # TypeScript interfaces
│   └── config/
│       └── settings.ts      # Configuration management
├── examples/                # Example notes and usage
│   ├── sample_note.md
│   └── mcp_config.json
└── docs/
    ├── SETUP.md            # Installation guide
    └── API.md              # MCP tools documentation
```

## Note Format Specification

### Markdown Structure

````markdown
---
created: 2025-06-14T10:30:00Z
updated: 2025-06-14T10:30:00Z
conversation_id: conv_12345
tags: [python, async, learning]
ai_client: claude-desktop
summary: Brief one-line description
---

# Conversation Title

## Key Learnings

Brief summary of main concepts discussed.

## Code Snippets

```python
# Relevant code examples with proper syntax highlighting
async def example_function():
    return "formatted code"
```
````

## Follow-up Questions

- Questions for future exploration
- Related topics to investigate

## References

- Links to documentation discussed
- Related notes in vault

````
### Frontmatter Schema

```typescript
interface NoteFrontmatter {
  created: string;           // ISO 8601 timestamp
  updated?: string;          // ISO 8601 timestamp
  conversation_id?: string;  // Unique conversation identifier
  tags: string[];           // Categorization tags
  ai_client?: string;       // Source AI client
  summary: string;          // One-line description
  related_notes?: string[]; // Links to related notes
}
````

### Note Naming Convention

Notes use kebab-case filenames without spaces:

- `python-async-patterns-2025-06-14.md`
- `react-hooks-best-practices.md`
- `api-design-conversation.md`

Format: `{topic-slug}-{optional-date}.md`

## Implementation Steps

### Phase 1: Core MCP Server (MVP)

1. **Setup Project Structure**
   - Initialize Deno project with `deno.json`
   - Create directory structure
   - Set up TypeScript configuration

2. **Implement Basic MCP Server**
   - Create main MCP server entry point
   - Implement server initialization and stdio communication
   - Add basic error handling and logging

3. **Develop Core Tools**
   - `create_note`: Basic note creation with frontmatter
   - `list_notes`: Simple file system listing
   - `get_note`: Read and return note content

4. **File System Integration**
   - Vault path configuration via environment variables
   - Safe filename generation (kebab-case, no spaces)
   - Markdown file creation with proper formatting
   - Git integration for automatic commits

### Phase 2: Enhanced Functionality

5. **Advanced Note Creation**
   - Intelligent content parsing and formatting
   - Code snippet extraction and syntax highlighting
   - Automatic tag suggestion based on content

6. **Search Implementation**
   - Full-text search across note content
   - Tag-based filtering and categorization
   - Relevance scoring and ranking

7. **Content Intelligence**
   - Duplicate detection and merging suggestions
   - Related note identification and linking
   - Conversation context preservation

### Phase 3: Polish and Integration

8. **Configuration System**
   - Environment variable configuration for vault path
   - Git configuration and commit message templates
   - User preference management
   - Vault-specific settings

9. **Error Handling and Validation**
   - Input validation and sanitization
   - Graceful failure modes and recovery
   - Comprehensive logging and debugging

10. **Documentation and Examples**
    - API documentation for all MCP tools
    - Usage examples and best practices
    - Integration guides for different AI clients

## Getting Started Checklist

### Prerequisites

- [ ] Install Deno: `curl -fsSL https://deno.land/install.sh | sh`
- [ ] Locate your existing Obsidian vault directory path
- [ ] Ensure git is initialized in your vault (if not: `cd /path/to/vault && git init`)
- [ ] Install Claude Desktop or other MCP-compatible client

### Configuration

- [ ] Set `OBSIDIAN_VAULT_PATH` environment variable to your vault location
- [ ] Optional: Set `GIT_COMMIT_TEMPLATE` for custom commit messages
- [ ] Configure Claude Desktop to include this MCP server
- [ ] Test vault write permissions and git access

### Claude Desktop Integration

Add to your Claude Desktop MCP configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "obsidian-notes": {
      "command": "deno",
      "args": [
        "run",
        "--allow-read",
        "--allow-write",
        "--allow-run",
        "--allow-env",
        "/path/to/obsidian-notes-mcp/src/main.ts"
      ],
      "env": {
        "OBSIDIAN_VAULT_PATH": "/path/to/your/obsidian/vault",
        "GIT_COMMIT_TEMPLATE": "Add note: %TITLE%"
      }
    }
  }
}
```

Replace `/path/to/obsidian-notes-mcp/src/main.ts` with the actual path to your MCP server.
Replace `/path/to/your/obsidian/vault` with your actual Obsidian vault path.

## Usage Examples

### Creating a Note via AI Chat

```
User: "Can you create a note summarizing our discussion about Python async patterns?"

AI: I'll create a note summarizing our Python async discussion.
[Calls create_note MCP tool with structured content]

Created note: "python-async-patterns-2025-06-14.md" in your Obsidian vault.
Git commit: abc123f - "Add AI conversation note: Python Async Patterns"
```

### Searching Previous Notes

```
User: "What did we learn about React hooks last month?"

AI: Let me search your notes for React hooks discussions.
[Calls search_notes MCP tool]

Found 3 relevant notes:
1. "react-hooks-best-practices-2025-05-15.md"
2. "custom-hook-patterns-2025-05-22.md"  
3. "useeffect-troubleshooting-2025-05-28.md"
```

## Development Notes

### TypeScript Learning Opportunities

This project provides excellent exposure to:

- Interface design and type safety
- Async/await patterns with proper typing
- File system operations with error handling
- JSON schema validation
- Module organization and dependency management

### MCP Protocol Benefits

- **Standardized**: Works across different AI clients
- **Local**: No cloud dependencies or API keys required
- **Extensible**: Easy to add new tools and capabilities
- **Secure**: Local file system access only

## Future Enhancements

### Potential Extensions

- **Telegram Bot Integration**: Create notes via messaging
- **Web Interface**: Browser-based note management
- **Advanced Search**: Vector search for semantic similarity
- **Note Templates**: Predefined formats for different note types
- **Export Tools**: Convert notes to other formats (PDF, HTML)
- **Collaboration**: Multi-user note sharing and synchronization

### Integration Possibilities

- **Git Integration**: Version control for note history
- **Calendar Sync**: Link notes to meeting schedules
- **Task Management**: Extract and track action items
- **Citation Management**: Academic reference handling
