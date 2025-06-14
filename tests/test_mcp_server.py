"""Tests for MCP server functionality."""

import pytest
from datetime import datetime, timedelta
from mcp_notes.main import MCPNotesServer
from mcp_notes.lib.date_parser import format_date_for_backlink


class TestMCPServer:
    """Test MCP server functionality."""
    
    @pytest.mark.asyncio
    async def test_create_note_basic(self, mcp_server, sample_note_params):
        """Test basic note creation."""
        result = await mcp_server._create_note(sample_note_params)
        
        assert len(result) == 1
        assert "Note created successfully" in result[0].text
        assert "test-note-" in result[0].text
        assert "committed to git" in result[0].text
    
    @pytest.mark.asyncio
    async def test_create_note_with_custom_date(self, mcp_server, sample_note_params):
        """Test note creation with custom date."""
        params = sample_note_params.copy()
        params["date_for"] = "yesterday"
        
        result = await mcp_server._create_note(params)
        
        assert len(result) == 1
        assert "Note created successfully" in result[0].text
        
        # Verify the note was created with yesterday's date
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        expected_filename = f"test-note-{yesterday}.md"
        assert expected_filename in result[0].text
    
    @pytest.mark.asyncio
    async def test_create_note_with_invalid_date(self, mcp_server, sample_note_params):
        """Test note creation with invalid date."""
        params = sample_note_params.copy()
        params["date_for"] = "invalid nonsense date"
        
        result = await mcp_server._create_note(params)
        
        assert len(result) == 1
        assert "Error: Could not parse date" in result[0].text
    
    @pytest.mark.asyncio
    async def test_create_duplicate_note(self, mcp_server, sample_note_params):
        """Test creating a duplicate note."""
        # Create first note
        await mcp_server._create_note(sample_note_params)
        
        # Try to create duplicate
        result = await mcp_server._create_note(sample_note_params)
        
        assert len(result) == 1
        assert "Error: Note with filename" in result[0].text
        assert "already exists" in result[0].text
    
    @pytest.mark.asyncio
    async def test_search_notes_empty(self, mcp_server):
        """Test searching notes when vault is empty."""
        result = await mcp_server._search_notes({"query": "test"})
        
        assert len(result) == 1
        assert "No notes found matching" in result[0].text
    
    @pytest.mark.asyncio
    async def test_search_notes_with_results(self, mcp_server, sample_note_params):
        """Test searching notes with results."""
        # Create a note first
        await mcp_server._create_note(sample_note_params)
        
        # Search for it
        result = await mcp_server._search_notes({"query": "test"})
        
        assert len(result) == 1
        assert "Found 1 note(s)" in result[0].text
        assert "Test Note" in result[0].text
    
    @pytest.mark.asyncio
    async def test_search_notes_with_tags(self, mcp_server, sample_note_params):
        """Test searching notes with tag filter."""
        # Create a note
        await mcp_server._create_note(sample_note_params)
        
        # Search with matching tag
        result = await mcp_server._search_notes({
            "query": "test",
            "tags": ["test"]
        })
        
        assert len(result) == 1
        assert "Found 1 note(s)" in result[0].text
        
        # Search with non-matching tag
        result = await mcp_server._search_notes({
            "query": "test",
            "tags": ["nonexistent"]
        })
        
        assert "No notes found" in result[0].text
    
    @pytest.mark.asyncio
    async def test_list_notes_empty(self, mcp_server):
        """Test listing notes when vault is empty."""
        result = await mcp_server._list_notes({})
        
        assert len(result) == 1
        assert "No notes found" in result[0].text
    
    @pytest.mark.asyncio
    async def test_list_notes_with_content(self, mcp_server, sample_note_params):
        """Test listing notes with content."""
        # Create a note
        await mcp_server._create_note(sample_note_params)
        
        # List notes
        result = await mcp_server._list_notes({})
        
        assert len(result) == 1
        assert "Found 1 total note(s)" in result[0].text
        assert "Test Note" in result[0].text
    
    @pytest.mark.asyncio
    async def test_get_note_existing(self, mcp_server, sample_note_params):
        """Test getting an existing note."""
        # Create a note
        create_result = await mcp_server._create_note(sample_note_params)
        
        # Extract filename from creation result (it should be in the format "Note created successfully: filename.md")
        text = create_result[0].text
        filename = None
        if "Note created successfully:" in text:
            # Extract filename from the message
            parts = text.split(":")
            if len(parts) > 1:
                filename_part = parts[1].strip()
                if filename_part.endswith(".md (committed to git)"):
                    filename = filename_part.replace(" (committed to git)", "")
                elif filename_part.endswith(".md"):
                    filename = filename_part
        
        assert filename is not None, f"Could not extract filename from: {text}"
        
        # Get the note
        result = await mcp_server._get_note({"filename": filename})
        
        assert len(result) == 1
        assert f"Content of {filename}" in result[0].text
        assert "Test Note" in result[0].text
    
    @pytest.mark.asyncio
    async def test_get_note_nonexistent(self, mcp_server):
        """Test getting a non-existent note."""
        result = await mcp_server._get_note({"filename": "nonexistent.md"})
        
        assert len(result) == 1
        assert "Note not found" in result[0].text
    
    @pytest.mark.asyncio
    async def test_note_contains_date_backlink(self, mcp_server, sample_note_params):
        """Test that created notes contain date backlinks."""
        # Create a note
        await mcp_server._create_note(sample_note_params)
        
        # List notes to get the filename
        list_result = await mcp_server._list_notes({})
        filename = None
        for line in list_result[0].text.split('\n'):
            if '.md' in line and 'File:' in line:
                filename = line.split('File:')[1].strip()
                break
        
        assert filename is not None
        
        # Get the note content
        get_result = await mcp_server._get_note({"filename": filename})
        content = get_result[0].text
        
        # Check for date backlink
        today = datetime.now().strftime('%Y-%m-%d')
        expected_backlink = f"Created: [[{today}]]"
        assert expected_backlink in content
    
    @pytest.mark.asyncio
    async def test_note_with_custom_date_backlink(self, mcp_server, sample_note_params):
        """Test that notes with custom dates have correct backlinks."""
        params = sample_note_params.copy()
        params["date_for"] = "2 days ago"
        
        # Create note with custom date
        await mcp_server._create_note(params)
        
        # List notes to get filename
        list_result = await mcp_server._list_notes({})
        filename = None
        for line in list_result[0].text.split('\n'):
            if '.md' in line and 'File:' in line:
                filename = line.split('File:')[1].strip()
                break
        
        assert filename is not None
        
        # Get note content
        get_result = await mcp_server._get_note({"filename": filename})
        content = get_result[0].text
        
        # Check for correct date backlink
        two_days_ago = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
        expected_backlink = f"Created: [[{two_days_ago}]]"
        assert expected_backlink in content