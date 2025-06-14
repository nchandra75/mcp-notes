# MCP Notes Server API Documentation

This document describes the Model Context Protocol (MCP) tools provided by the Obsidian Notes server.

## Overview

The MCP Notes server provides four main tools for managing markdown notes in Obsidian vaults:

1. **`create_note`** - Create new conversation summaries and notes
2. **`search_notes`** - Search through existing notes using full-text search
3. **`list_notes`** - Browse and filter your note collection
4. **`get_note`** - Retrieve the full content of specific notes

All notes are created with YAML frontmatter and stored as markdown files using kebab-case naming conventions.

## Tools Reference

### create_note

Creates a new markdown note with YAML frontmatter in your Obsidian vault.

#### Parameters

| Parameter         | Type     | Required | Description                                         |
| ----------------- | -------- | -------- | --------------------------------------------------- |
| `title`           | string   | ✅       | Title of the note                                   |
| `content`         | string   | ✅       | Main content of the note in markdown format         |
| `tags`            | string[] | ❌       | Array of tags to categorize the note                |
| `conversation_id` | string   | ❌       | Unique identifier for the conversation              |
| `ai_client`       | string   | ❌       | Name of the AI client used (e.g., "claude-desktop") |
| `summary`         | string   | ❌       | Brief one-line summary of the note content          |

#### Example Usage

````typescript
// Creating a comprehensive note
{
  "title": "Python Async Patterns",
  "content": "# Python Async Patterns\n\n## Key Learnings\n\n- Use `asyncio.gather()` for concurrent execution\n- `async with` for async context managers\n- Avoid blocking calls in async functions\n\n## Code Example\n\n```python\nimport asyncio\n\nasync def fetch_data(url):\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as response:\n            return await response.json()\n```\n\n## Follow-up Questions\n\n- How to handle exceptions in async code?\n- Best practices for async database operations?",
  "tags": ["python", "async", "programming", "best-practices"],
  "conversation_id": "conv_20250614_001",
  "ai_client": "claude-desktop",
  "summary": "Discussion about Python async/await patterns and best practices"
}
````

#### Response

```json
{
  "content": [
    {
      "type": "text",
      "text": "Note created successfully:\n\nFilename: python-async-patterns-2025-06-14.md\nPath: /path/to/vault/python-async-patterns-2025-06-14.md\nGit commit: abc123f\n\nThe note has been saved to your Obsidian vault and is ready to use."
    }
  ]
}
```

#### Generated Frontmatter

```yaml
---
created: 2025-06-14T10:30:00.000Z
updated: 2025-06-14T10:30:00.000Z
conversation_id: conv_20250614_001
tags: [python, async, programming, best-practices]
ai_client: claude-desktop
summary: Discussion about Python async/await patterns and best practices
---
```

### search_notes

Search through existing notes using full-text search with relevance scoring.

#### Parameters

| Parameter | Type     | Required | Description                                       |
| --------- | -------- | -------- | ------------------------------------------------- |
| `query`   | string   | ✅       | Search query text                                 |
| `tags`    | string[] | ❌       | Filter results by specific tags                   |
| `limit`   | number   | ❌       | Maximum number of results to return (default: 10) |

#### Search Algorithm

The search engine scores results based on:

- **Title matches** (3x weight) - Exact or partial title matches
- **Summary matches** (2x weight) - Matches in the frontmatter summary
- **Content matches** (1x weight) - Matches in the note body
- **Tag matches** (1.5x weight) - Matches in note tags

#### Example Usage

```typescript
// Basic search
{
  "query": "async patterns",
  "limit": 5
}

// Search with tag filtering
{
  "query": "database",
  "tags": ["python", "tutorial"],
  "limit": 10
}
```

#### Response

```json
{
  "content": [
    {
      "type": "text",
      "text": "Found 3 notes matching \"async patterns\":\n\n1. **python-async-patterns-2025-06-14.md** (Score: 8.5)\n   Summary: Discussion about Python async/await patterns and best practices\n   Tags: python, async, programming, best-practices\n   Created: 6/14/2025\n   Matches: Title: python-async-patterns; Content: Use asyncio.gather() for concurrent execution\n\n2. **javascript-promises-vs-async-2025-06-10.md** (Score: 6.2)\n   Summary: Comparison between Promises and async/await in JavaScript\n   Tags: javascript, async, promises\n   Created: 6/10/2025\n   Matches: Content: async/await provides cleaner syntax than Promises\n\n3. **async-debugging-tips-2025-06-08.md** (Score: 4.1)\n   Summary: Tips for debugging asynchronous code\n   Tags: debugging, async, development\n   Created: 6/8/2025\n   Matches: Tags: async; Content: debugging asynchronous patterns"
    }
  ]
}
```

### list_notes

Browse and filter your note collection with sorting options.

#### Parameters

| Parameter | Type     | Required | Description                                                       |
| --------- | -------- | -------- | ----------------------------------------------------------------- |
| `tags`    | string[] | ❌       | Filter by specific tags                                           |
| `limit`   | number   | ❌       | Maximum number of notes to return (default: 20)                   |
| `sort`    | string   | ❌       | Sort field: "created", "updated", or "title" (default: "updated") |
| `order`   | string   | ❌       | Sort order: "asc" or "desc" (default: "desc")                     |

#### Example Usage

```typescript
// List recent notes
{
  "limit": 10,
  "sort": "updated",
  "order": "desc"
}

// List notes by tag
{
  "tags": ["python", "tutorial"],
  "sort": "created",
  "order": "asc"
}

// List all notes alphabetically
{
  "sort": "title",
  "order": "asc"
}
```

#### Response

```json
{
  "content": [
    {
      "type": "text",
      "text": "Found 15 notes in your vault:\n\n1. **python-async-patterns-2025-06-14.md**\n   Summary: Discussion about Python async/await patterns and best practices\n   Tags: python, async, programming, best-practices\n   Created: 6/14/2025\n   Updated: 6/14/2025\n\n2. **react-hooks-guide-2025-06-13.md**\n   Summary: Comprehensive guide to React hooks and their usage\n   Tags: react, javascript, hooks, frontend\n   Created: 6/13/2025\n   Updated: 6/13/2025\n\n3. **database-optimization-tips-2025-06-12.md**\n   Summary: Database query optimization techniques and best practices\n   Tags: database, sql, optimization, performance\n   Created: 6/12/2025\n   Updated: 6/12/2025"
    }
  ]
}
```

### get_note

Retrieve the full content of a specific note by filename.

#### Parameters

| Parameter  | Type   | Required | Description                                                |
| ---------- | ------ | -------- | ---------------------------------------------------------- |
| `filename` | string | ✅       | Filename of the note to retrieve (including .md extension) |

#### Example Usage

```typescript
{
  "filename": "python-async-patterns-2025-06-14.md"
}
```

#### Response

````json
{
  "content": [
    {
      "type": "text",
      "text": "**python-async-patterns-2025-06-14.md**\n\n**Frontmatter:**\ncreated: 2025-06-14T10:30:00.000Z\nupdated: 2025-06-14T10:30:00.000Z\nconversation_id: conv_20250614_001\ntags: python, async, programming, best-practices\nai_client: claude-desktop\nsummary: Discussion about Python async/await patterns and best practices\n\n**Content:**\n# Python Async Patterns\n\n## Key Learnings\n\n- Use `asyncio.gather()` for concurrent execution\n- `async with` for async context managers\n- Avoid blocking calls in async functions\n\n## Code Example\n\n```python\nimport asyncio\n\nasync def fetch_data(url):\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as response:\n            return await response.json()\n```\n\n## Follow-up Questions\n\n- How to handle exceptions in async code?\n- Best practices for async database operations?"
    }
  ]
}
````

## Note Format Specification

### File Naming Convention

Notes use kebab-case filenames with optional date suffixes:

- `{topic-slug}-{date}.md` (e.g., `python-async-patterns-2025-06-14.md`)
- `{topic-slug}.md` (e.g., `react-hooks-guide.md`)

The server automatically:

- Converts titles to kebab-case
- Removes special characters
- Adds current date to avoid conflicts
- Ensures `.md` extension

### Frontmatter Schema

All notes include YAML frontmatter with these fields:

```yaml
---
created: "2025-06-14T10:30:00.000Z"     # ISO 8601 timestamp (required)
updated: "2025-06-14T10:30:00.000Z"     # ISO 8601 timestamp (required)
conversation_id: "conv_12345"           # Optional conversation identifier
tags: ["python", "async", "learning"]  # Array of tags (required, can be empty)
ai_client: "claude-desktop"             # Optional AI client identifier
summary: "Brief description"            # Required summary text
---
```

### Content Structure

While content structure is flexible, the following format is recommended for conversation summaries:

````markdown
# Title

## Key Learnings

- Main concepts and insights
- Important takeaways

## Code Snippets

```language
// Code examples with proper syntax highlighting
```
````

## Follow-up Questions

- Questions for future exploration
- Related topics to investigate

## References

- Links to documentation
- Related notes in vault

````
## Error Handling

### Common Errors

1. **Missing vault path**: Server exits if `OBSIDIAN_VAULT_PATH` is not set
2. **File not found**: `get_note` returns friendly error message for missing files
3. **Permission denied**: File system errors are caught and reported
4. **Invalid parameters**: Type validation errors for missing required fields

### Error Response Format

```json
{
  "error": {
    "code": 1,
    "message": "Tool execution failed: Note not found: nonexistent-file.md"
  }
}
````

## Best Practices

### Creating Effective Notes

1. **Use descriptive titles** - Help with search and organization
2. **Add relevant tags** - Enable better filtering and discovery
3. **Write clear summaries** - One-line descriptions for quick scanning
4. **Structure content** - Use headings and lists for readability
5. **Include conversation context** - Add conversation_id for tracking

### Search Optimization

1. **Use specific terms** - More specific queries yield better results
2. **Combine search with tags** - Filter results for better precision
3. **Check spelling** - Exact matches score higher than partial matches
4. **Use title keywords** - Title matches have highest relevance scores

### Organization Tips

1. **Consistent tagging** - Develop a tag taxonomy for your notes
2. **Regular cleanup** - Use `list_notes` to review and organize
3. **Meaningful filenames** - The auto-generated names are based on titles
4. **Date-based sorting** - Use `sort: "updated"` to find recent work

## Integration Examples

### Claude Desktop Workflow

```
User: "Can you create a note summarizing our discussion about React performance optimization?"

Claude: I'll create a note about our React performance discussion.
[Calls create_note with structured content]

User: "What other React notes do I have?"

Claude: Let me search for your React-related notes.
[Calls search_notes with query "React"]

User: "Show me the content of that hooks guide note"

Claude: I'll retrieve the React hooks guide for you.
[Calls get_note with specific filename]
```

### Development Workflow

1. **Conversation Summary**: Create notes after productive AI conversations
2. **Knowledge Base**: Search existing notes before asking repeated questions
3. **Reference Material**: Use notes as quick reference for code patterns
4. **Learning Journal**: Track progress and insights over time

For setup instructions and troubleshooting, see [SETUP.md](./SETUP.md).
