"""Configuration settings for MCP Notes."""

import os
from pathlib import Path
from typing import Optional


def get_vault_path() -> str:
    """Get the Obsidian vault path from environment."""
    vault_path = os.getenv('OBSIDIAN_VAULT_PATH')
    if not vault_path:
        raise ValueError("OBSIDIAN_VAULT_PATH environment variable is required")
    
    # Expand user path if needed
    vault_path = Path(vault_path).expanduser().absolute()
    return str(vault_path)


def get_git_commit_template() -> Optional[str]:
    """Get custom git commit message template."""
    return os.getenv('GIT_COMMIT_TEMPLATE')