"""Tests for file manager functionality."""

import pytest
from pathlib import Path
from mcp_notes.lib.file_manager import FileManager


class TestFileManager:
    """Test file manager functionality."""
    
    def test_init_file_manager(self, temp_vault):
        """Test initializing file manager."""
        file_manager = FileManager(temp_vault)
        assert file_manager.vault_path == Path(temp_vault)
        assert file_manager.vault_path.exists()
    
    def test_generate_filename(self, temp_vault):
        """Test filename generation."""
        file_manager = FileManager(temp_vault)
        
        result = file_manager.generate_filename("Test Note")
        assert result.startswith("test-note-")
        assert result.endswith(".md")
    
    def test_get_note_path(self, temp_vault):
        """Test getting note path."""
        file_manager = FileManager(temp_vault)
        filename = "test-note.md"
        
        result = file_manager.get_note_path(filename)
        expected = Path(temp_vault) / filename
        
        assert result == expected
    
    def test_note_exists(self, temp_vault):
        """Test checking if note exists."""
        file_manager = FileManager(temp_vault)
        filename = "test-note.md"
        
        # Note doesn't exist initially
        assert not file_manager.note_exists(filename)
        
        # Create the note
        note_path = file_manager.get_note_path(filename)
        note_path.write_text("Test content")
        
        # Now it should exist
        assert file_manager.note_exists(filename)
    
    def test_write_and_read_note(self, temp_vault):
        """Test writing and reading notes."""
        file_manager = FileManager(temp_vault)
        filename = "test-note.md"
        content = "# Test Note\n\nThis is test content."
        
        # Write note
        file_manager.write_note(filename, content)
        
        # Verify it exists
        assert file_manager.note_exists(filename)
        
        # Read it back
        result = file_manager.read_note(filename)
        assert result == content
    
    def test_read_nonexistent_note(self, temp_vault):
        """Test reading a note that doesn't exist."""
        file_manager = FileManager(temp_vault)
        
        with pytest.raises(FileNotFoundError):
            file_manager.read_note("nonexistent.md")
    
    def test_list_notes(self, temp_vault):
        """Test listing notes."""
        file_manager = FileManager(temp_vault)
        
        # Initially empty
        notes = file_manager.list_notes()
        assert notes == []
        
        # Create some notes
        file_manager.write_note("note1.md", "Content 1")
        file_manager.write_note("note2.md", "Content 2")
        file_manager.write_note("note3.md", "Content 3")
        
        # Create a non-markdown file (should be ignored)
        (Path(temp_vault) / "other.txt").write_text("Not markdown")
        
        # List notes
        notes = file_manager.list_notes()
        assert len(notes) == 3
        assert "note1.md" in notes
        assert "note2.md" in notes
        assert "note3.md" in notes
        assert "other.txt" not in notes
    
    def test_delete_note(self, temp_vault):
        """Test deleting notes."""
        file_manager = FileManager(temp_vault)
        filename = "test-note.md"
        
        # Create and verify note
        file_manager.write_note(filename, "Test content")
        assert file_manager.note_exists(filename)
        
        # Delete note
        file_manager.delete_note(filename)
        assert not file_manager.note_exists(filename)
        
        # Deleting non-existent note should not raise error
        file_manager.delete_note("nonexistent.md")
    
    def test_get_note_stats(self, temp_vault):
        """Test getting note statistics."""
        file_manager = FileManager(temp_vault)
        filename = "test-note.md"
        content = "Test content for stats"
        
        # Create note
        file_manager.write_note(filename, content)
        
        # Get stats
        stats = file_manager.get_note_stats(filename)
        
        assert "size" in stats
        assert "created" in stats
        assert "modified" in stats
        assert stats["size"] == len(content.encode('utf-8'))
    
    def test_get_stats_nonexistent_note(self, temp_vault):
        """Test getting stats for non-existent note."""
        file_manager = FileManager(temp_vault)
        
        with pytest.raises(FileNotFoundError):
            file_manager.get_note_stats("nonexistent.md")