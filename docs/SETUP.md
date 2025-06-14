# MCP Notes Server Setup Guide

This guide will help you set up and configure the MCP Notes server to work with Claude Desktop and other MCP-compatible AI clients.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Deno Runtime**: [Install Deno](https://deno.land/install.sh)
- **Git**: For version control integration (optional but recommended)
- **Obsidian**: The notes will be saved as markdown files in your Obsidian vault
- **Claude Desktop**: Or another MCP-compatible AI client

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nchandra75/mcp-notes.git
cd mcp-notes
```

### 2. Verify Deno Installation

```bash
deno --version
```

You should see output showing Deno version 2.0 or higher.

### 3. Test the Server

```bash
# Check TypeScript compilation
deno check src/main.ts

# Test the server (it will exit quickly without stdio input)
OBSIDIAN_VAULT_PATH="/path/to/your/vault" deno run --allow-read --allow-write --allow-run --allow-env src/main.ts
```

## Configuration

### Environment Variables

The server requires one mandatory environment variable:

- **`OBSIDIAN_VAULT_PATH`** (Required): Full path to your Obsidian vault directory
- **`GIT_COMMIT_TEMPLATE`** (Optional): Custom git commit message template

Example:

```bash
export OBSIDIAN_VAULT_PATH="/Users/username/Documents/MyVault"
export GIT_COMMIT_TEMPLATE="Add AI conversation note: %TITLE%"
```

### Vault Preparation

1. **Create or locate your Obsidian vault directory**
2. **Initialize git repository** (recommended):
   ```bash
   cd /path/to/your/vault
   git init
   git add .
   git commit -m "Initial vault setup"
   ```
3. **Test write permissions**:
   ```bash
   touch /path/to/your/vault/test-file.md
   rm /path/to/your/vault/test-file.md
   ```

## Claude Desktop Integration

### 1. Locate Claude Desktop Configuration

Find your Claude Desktop configuration file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### 2. Add MCP Server Configuration

Edit the configuration file and add the MCP Notes server:

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
        "/full/path/to/mcp-notes/src/main.ts"
      ],
      "env": {
        "OBSIDIAN_VAULT_PATH": "/full/path/to/your/obsidian/vault",
        "GIT_COMMIT_TEMPLATE": "Add note: %TITLE%"
      }
    }
  }
}
```

**Important**: Replace the paths with your actual file system paths:

- `/full/path/to/mcp-notes/src/main.ts` → Your MCP server location
- `/full/path/to/your/obsidian/vault` → Your Obsidian vault location

### 3. Restart Claude Desktop

Close and restart Claude Desktop for the changes to take effect.

### 4. Verify Integration

Open Claude Desktop and start a new conversation. The MCP Notes tools should now be available:

- `create_note` - Create new notes from conversations
- `search_notes` - Search existing notes
- `list_notes` - Browse your note collection
- `get_note` - Retrieve specific note content

## Testing the Setup

### Basic Functionality Test

1. **Create a test note**:
   ```
   User: "Can you create a note about setting up the MCP server?"

   Claude: I'll create a note about our MCP server setup discussion.
   ```

2. **List existing notes**:
   ```
   User: "What notes do I have in my vault?"

   Claude: Let me list your current notes.
   ```

3. **Search for content**:
   ```
   User: "Search for notes about MCP"

   Claude: I'll search your notes for MCP-related content.
   ```

### Troubleshooting

#### Common Issues

1. **"OBSIDIAN_VAULT_PATH environment variable is required"**
   - Ensure the path is correctly set in the Claude Desktop config
   - Use absolute paths, not relative paths
   - Check that the directory exists

2. **Permission denied errors**
   - Verify Deno has read/write access to the vault directory
   - Check file system permissions on the vault folder

3. **Git commit failures**
   - Ensure git is initialized in your vault directory
   - Check that git user.name and user.email are configured:
     ```bash
     git config --global user.name "Your Name"
     git config --global user.email "your.email@example.com"
     ```

4. **Notes not appearing in Obsidian**
   - Refresh Obsidian or restart it
   - Check that files are being created in the correct vault directory
   - Verify the vault path matches your Obsidian vault location

#### Debug Mode

To debug issues, you can run the server manually with logging:

```bash
OBSIDIAN_VAULT_PATH="/path/to/vault" deno run --allow-read --allow-write --allow-run --allow-env src/main.ts
```

The server will show startup messages and any errors in the console.

## Advanced Configuration

### Custom Commit Messages

You can customize git commit messages using the `GIT_COMMIT_TEMPLATE` environment variable:

```bash
# Default template
GIT_COMMIT_TEMPLATE="Add note: %TITLE%"

# Custom templates
GIT_COMMIT_TEMPLATE="📝 AI conversation: %TITLE%"
GIT_COMMIT_TEMPLATE="[AI] %TITLE% - $(date +%Y-%m-%d)"
```

The `%TITLE%` placeholder will be replaced with the actual note title.

### Multiple Vault Support

To use multiple vaults, create separate MCP server configurations:

```json
{
  "mcpServers": {
    "obsidian-work": {
      "command": "deno",
      "args": [
        "run",
        "--allow-read",
        "--allow-write",
        "--allow-run",
        "--allow-env",
        "/path/to/mcp-notes/src/main.ts"
      ],
      "env": {
        "OBSIDIAN_VAULT_PATH": "/path/to/work/vault"
      }
    },
    "obsidian-personal": {
      "command": "deno",
      "args": [
        "run",
        "--allow-read",
        "--allow-write",
        "--allow-run",
        "--allow-env",
        "/path/to/mcp-notes/src/main.ts"
      ],
      "env": {
        "OBSIDIAN_VAULT_PATH": "/path/to/personal/vault"
      }
    }
  }
}
```

## Next Steps

Once your setup is complete:

1. **Start using the tools** - Create notes from your AI conversations
2. **Explore search functionality** - Find relevant past conversations
3. **Organize with tags** - Use tags to categorize your notes
4. **Review API documentation** - See [API.md](./API.md) for detailed tool usage

For more examples and usage patterns, check out the [examples](../examples/) directory.
