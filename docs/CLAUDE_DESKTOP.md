# Claude Desktop Integration Guide

This guide provides detailed instructions for integrating the MCP Notes server with Claude Desktop, including configuration, troubleshooting, and usage examples.

## Quick Setup

### 1. Find Your Configuration File

Claude Desktop stores its configuration in different locations depending on your operating system:

**macOS:**

```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**

```cmd
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**

```bash
~/.config/Claude/claude_desktop_config.json
```

### 2. Create or Edit Configuration

If the file doesn't exist, create it. If it exists, add the MCP server configuration to the existing `mcpServers` section.

**New Configuration File:**

```json
{
  "mcpServers": {
    "obsidian-notes": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/mcp-notes",
        "src/mcp_notes/main.py"
      ],
      "env": {
        "OBSIDIAN_VAULT_PATH": "/absolute/path/to/your/obsidian/vault",
        "GIT_COMMIT_TEMPLATE": "Add AI note: {title}"
      }
    }
  }
}
```

**Adding to Existing Configuration:**

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "existing-command",
      "args": ["existing", "args"]
    },
    "obsidian-notes": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/mcp-notes",
        "src/mcp_notes/main.py"
      ],
      "env": {
        "OBSIDIAN_VAULT_PATH": "/absolute/path/to/your/obsidian/vault",
        "GIT_COMMIT_TEMPLATE": "Add AI note: {title}"
      }
    }
  }
}
```

### 3. Update Paths

Replace the placeholder paths with your actual file system paths:

1. **MCP Server Path**: Find where you cloned/downloaded the mcp-notes repository
   ```bash
   # Example paths:
   # macOS: /Users/username/Documents/mcp-notes/src/main.ts
   # Windows: C:\Users\username\Documents\mcp-notes\src\main.ts
   # Linux: /home/username/mcp-notes/src/main.ts
   ```

2. **Obsidian Vault Path**: Find your Obsidian vault directory
   ```bash
   # Example paths:
   # macOS: /Users/username/Documents/ObsidianVault
   # Windows: C:\Users\username\Documents\ObsidianVault
   # Linux: /home/username/Documents/ObsidianVault
   ```

### 4. Restart Claude Desktop

Close Claude Desktop completely and restart it for the configuration changes to take effect.

## Configuration Options

### Required Settings

| Setting               | Description                              | Example                           |
| --------------------- | ---------------------------------------- | --------------------------------- |
| `command`             | Deno executable                          | `"deno"`                          |
| `args`                | Command arguments for running the server | See configuration above           |
| `OBSIDIAN_VAULT_PATH` | Absolute path to your Obsidian vault     | `"/Users/john/Documents/MyVault"` |

### Optional Settings

| Setting               | Description                        | Default               | Example                         |
| --------------------- | ---------------------------------- | --------------------- | ------------------------------- |
| `GIT_COMMIT_TEMPLATE` | Custom git commit message template | `"Add note: {title}"` | `"📝 AI conversation: {title}"` |

### Permission Flags

The Deno server requires specific permissions:

- `--allow-read` - Read files from the vault directory
- `--allow-write` - Write new notes and modify existing ones
- `--allow-run` - Execute git commands for version control
- `--allow-env` - Access environment variables for configuration

## Platform-Specific Setup

### macOS Setup

1. **Install Deno** (if not already installed):
   ```bash
   curl -fsSL https://deno.land/install.sh | sh
   ```

2. **Find your vault path**:
   ```bash
   # If using iCloud
   ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/VaultName

   # If using local storage
   ~/Documents/ObsidianVault
   ```

3. **Example configuration**:
   ```json
   {
     "mcpServers": {
       "obsidian-notes": {
         "command": "uv",
         "args": [
           "run",
           "--directory",
           "/Users/john/Documents/mcp-notes",
           "src/mcp_notes/main.py"
         ],
         "env": {
           "OBSIDIAN_VAULT_PATH": "/Users/john/Documents/MyVault",
           "GIT_COMMIT_TEMPLATE": "Add note: {title}"
         }
       }
     }
   }
   ```

### Windows Setup

1. **Install Deno** (if not already installed):
   ```powershell
   iwr https://deno.land/install.ps1 -useb | iex
   ```

2. **Find your vault path**:
   ```cmd
   # Common locations
   C:\Users\YourName\Documents\ObsidianVault
   C:\Users\YourName\OneDrive\Documents\ObsidianVault
   ```

3. **Example configuration** (use forward slashes or escaped backslashes):
   ```json
   {
     "mcpServers": {
       "obsidian-notes": {
         "command": "uv",
         "args": [
           "run",
           "--directory",
           "C:/Users/john/Documents/mcp-notes",
           "src/mcp_notes/main.py"
         ],
         "env": {
           "OBSIDIAN_VAULT_PATH": "C:/Users/john/Documents/MyVault",
           "GIT_COMMIT_TEMPLATE": "Add note: {title}"
         }
       }
     }
   }
   ```

### Linux Setup

1. **Install Deno** (if not already installed):
   ```bash
   curl -fsSL https://deno.land/install.sh | sh
   ```

2. **Find your vault path**:
   ```bash
   # Common locations
   ~/Documents/ObsidianVault
   ~/vault
   ```

3. **Example configuration**:
   ```json
   {
     "mcpServers": {
       "obsidian-notes": {
         "command": "uv",
         "args": [
           "run",
           "--directory",
           "/home/john/mcp-notes",
           "src/mcp_notes/main.py"
         ],
         "env": {
           "OBSIDIAN_VAULT_PATH": "/home/john/Documents/MyVault",
           "GIT_COMMIT_TEMPLATE": "Add note: {title}"
         }
       }
     }
   }
   ```

## Testing the Integration

### 1. Verify Claude Desktop Startup

1. Open Claude Desktop
2. Start a new conversation
3. Check that no error messages appear related to MCP servers

### 2. Test Basic Functionality

Try these commands in Claude Desktop:

**Create a test note:**

```
Can you create a note titled "MCP Server Test" with some basic content about testing the setup?
```

**List existing notes:**

```
What notes do I currently have in my vault?
```

**Search functionality:**

```
Search for notes containing "test" or "setup"
```

### 3. Verify File Creation

1. Check your Obsidian vault directory
2. Look for newly created `.md` files
3. Open the files to verify proper formatting
4. Check git history if using version control

## Troubleshooting

### Common Issues

#### 1. "MCP Server Failed to Start"

**Symptoms:** Claude Desktop shows error about MCP server startup failure

**Solutions:**

- Verify Deno is installed and in PATH: `deno --version`
- Check that file paths in configuration are absolute and correct
- Ensure the mcp-notes repository is downloaded and `src/main.ts` exists
- Verify JSON syntax in configuration file

#### 2. "OBSIDIAN_VAULT_PATH environment variable is required"

**Symptoms:** Server starts but immediately exits with this error

**Solutions:**

- Check that `OBSIDIAN_VAULT_PATH` is set in the `env` section
- Verify the vault path exists and is accessible
- Use absolute paths, not relative paths
- Ensure proper JSON escaping for Windows paths

#### 3. "Permission denied" or File Access Errors

**Symptoms:** Server starts but fails when trying to create notes

**Solutions:**

- Check file system permissions on vault directory
- Ensure Claude Desktop/Deno has write access to the vault
- Verify vault directory is not read-only
- On Windows, check if antivirus is blocking file writes

#### 4. Git Commit Failures

**Symptoms:** Notes are created but git commits fail

**Solutions:**

- Initialize git in vault directory: `git init`
- Configure git user:
  ```bash
  git config user.name "Your Name"
  git config user.email "your.email@example.com"
  ```
- Ensure git is installed and in PATH
- Check vault directory has write permissions for git

#### 5. Notes Not Appearing in Obsidian

**Symptoms:** Server reports success but files don't appear in Obsidian

**Solutions:**

- Refresh Obsidian vault view
- Check if vault path matches Obsidian's configured vault
- Verify files are created in correct directory
- Restart Obsidian if needed

### Debug Mode

To debug configuration issues:

1. **Test Deno command manually:**
   ```bash
   cd /path/to/vault
   OBSIDIAN_VAULT_PATH="/path/to/vault" deno run --allow-read --allow-write --allow-run --allow-env /path/to/mcp-notes/src/main.ts
   ```

2. **Check Claude Desktop logs:**
   - macOS: Check Console app for Claude Desktop logs
   - Windows: Check Event Viewer or application logs
   - Linux: Check system logs with `journalctl`

3. **Validate JSON configuration:**
   ```bash
   # Use a JSON validator tool or online service
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python -m json.tool
   ```

## Advanced Configuration

### Multiple Vaults

To work with multiple Obsidian vaults, create separate MCP server configurations:

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

### Custom Git Configuration

Customize git commit messages and behavior:

```json
{
  "env": {
    "OBSIDIAN_VAULT_PATH": "/path/to/vault",
    "GIT_COMMIT_TEMPLATE": "📝 [AI] {title} - $(date +%Y-%m-%d)",
    "GIT_AUTO_PUSH": "false"
  }
}
```

## Usage Examples

### Creating Conversation Summaries

```
User: "Can you create a note summarizing our discussion about React hooks? Include the key points about useState, useEffect, and custom hooks."

Claude: I'll create a comprehensive note about our React hooks discussion.

[Uses create_note tool to create structured note with:
- Title: "React Hooks Discussion"
- Content: Formatted markdown with sections for each hook type
- Tags: ["react", "hooks", "javascript", "frontend"]
- Summary: "Discussion about React hooks including useState, useEffect, and custom hooks"]

Note created: react-hooks-discussion-2025-06-14.md
```

### Knowledge Base Search

```
User: "What did we discuss about async programming in Python?"

Claude: Let me search your notes for Python async discussions.

[Uses search_notes tool with query "Python async"]

Found 3 relevant notes:
1. python-async-patterns-2025-06-10.md
2. asyncio-troubleshooting-2025-06-08.md
3. python-concurrent-programming-2025-06-05.md
```

### Note Organization

```
User: "Show me all my Python-related notes from this month"

Claude: I'll list your Python notes with recent dates.

[Uses list_notes tool with tags filter and date sorting]

Found 8 Python notes from June 2025:
- python-async-patterns-2025-06-14.md
- python-decorators-guide-2025-06-12.md
- python-testing-strategies-2025-06-10.md
...
```

## Security Considerations

### File System Access

The MCP server requires read/write access to your Obsidian vault. Consider:

- Use dedicated vault directories for AI-generated content
- Regular backups of important notes
- Git version control for change tracking
- Review generated content before committing to version control

### Environment Variables

- Store sensitive paths in environment variables, not hardcoded in config
- Use appropriate file system permissions
- Consider using dedicated user accounts for automation

For more detailed API documentation, see [API.md](./API.md). For general setup instructions, see [SETUP.md](./SETUP.md).
