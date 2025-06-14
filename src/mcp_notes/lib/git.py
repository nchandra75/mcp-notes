"""Git operations for note version control."""

import os
from pathlib import Path
from typing import Optional

from git import Repo, InvalidGitRepositoryError


class GitManager:
    """Manages git operations for notes."""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self._repo: Optional[Repo] = None
        self._init_repo()
    
    def _init_repo(self) -> None:
        """Initialize or open git repository."""
        try:
            self._repo = Repo(self.vault_path)
        except InvalidGitRepositoryError:
            # Initialize new repository
            self._repo = Repo.init(self.vault_path)
            self._configure_repo()
    
    def _configure_repo(self) -> None:
        """Configure git repository with default settings."""
        if not self._repo:
            return
        
        config = self._repo.config_writer()
        
        # Set default user if not configured
        try:
            self._repo.config_reader().get_value("user", "name")
        except:
            config.set_value("user", "name", "MCP Notes Server")
        
        try:
            self._repo.config_reader().get_value("user", "email")
        except:
            config.set_value("user", "email", "mcp-notes@example.com")
        
        config.release()
    
    def commit_note(self, filename: str, message: Optional[str] = None) -> bool:
        """Commit a note file to git."""
        if not self._repo:
            return False
        
        try:
            # Add the specific file
            self._repo.index.add([filename])
            
            # Create commit message
            if not message:
                message = f"Add note: {filename}"
            
            # Commit the changes
            self._repo.index.commit(message)
            return True
            
        except Exception as e:
            print(f"Git commit failed: {e}")
            return False
    
    def is_repo_clean(self) -> bool:
        """Check if repository has no uncommitted changes."""
        if not self._repo:
            return True
        return not self._repo.is_dirty()
    
    def get_commit_history(self, filename: Optional[str] = None, limit: int = 10) -> list:
        """Get commit history for a file or entire repository."""
        if not self._repo:
            return []
        
        try:
            if filename:
                commits = list(self._repo.iter_commits(paths=filename, max_count=limit))
            else:
                commits = list(self._repo.iter_commits(max_count=limit))
            
            return [
                {
                    'sha': commit.hexsha[:8],
                    'message': commit.message.strip(),
                    'author': str(commit.author),
                    'date': commit.committed_datetime.isoformat(),
                }
                for commit in commits
            ]
        except Exception:
            return []