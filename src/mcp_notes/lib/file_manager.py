"""File management utilities for notes."""

import os
from pathlib import Path
from typing import List, Optional

from .markdown import generate_filename, kebab_case


class FileManager:
    """Manages file operations for notes."""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.vault_path.mkdir(parents=True, exist_ok=True)
    
    def generate_filename(self, title: str) -> str:
        """Generate a safe filename from title."""
        return generate_filename(title)
    
    def get_note_path(self, filename: str) -> Path:
        """Get full path for a note file."""
        return self.vault_path / filename
    
    def note_exists(self, filename: str) -> bool:
        """Check if a note file exists."""
        return self.get_note_path(filename).exists()
    
    def write_note(self, filename: str, content: str) -> None:
        """Write note content to file."""
        note_path = self.get_note_path(filename)
        note_path.write_text(content, encoding='utf-8')
    
    def read_note(self, filename: str) -> str:
        """Read note content from file."""
        note_path = self.get_note_path(filename)
        if not note_path.exists():
            raise FileNotFoundError(f"Note not found: {filename}")
        return note_path.read_text(encoding='utf-8')
    
    def list_notes(self) -> List[str]:
        """List all markdown note files."""
        notes = []
        for file_path in self.vault_path.glob("*.md"):
            notes.append(file_path.name)
        return sorted(notes)
    
    def delete_note(self, filename: str) -> None:
        """Delete a note file."""
        note_path = self.get_note_path(filename)
        if note_path.exists():
            note_path.unlink()
    
    def get_note_stats(self, filename: str) -> dict:
        """Get file statistics for a note."""
        note_path = self.get_note_path(filename)
        if not note_path.exists():
            raise FileNotFoundError(f"Note not found: {filename}")
        
        stat = note_path.stat()
        return {
            'size': stat.st_size,
            'created': stat.st_ctime,
            'modified': stat.st_mtime,
        }