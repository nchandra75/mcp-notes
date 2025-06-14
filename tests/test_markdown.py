"""Tests for markdown functionality."""

import pytest
from datetime import datetime
from mcp_notes.lib.markdown import (
    parse_markdown, format_markdown, create_default_frontmatter,
    extract_title_from_content, kebab_case, generate_filename
)
from mcp_notes.lib.types import NoteFrontmatter


class TestMarkdown:
    """Test markdown functionality."""
    
    def test_parse_markdown_with_frontmatter(self):
        """Test parsing markdown with valid frontmatter."""
        content = """---
created: '2025-06-14T10:30:00.000Z'
updated: '2025-06-14T10:30:00.000Z'
tags:
- test
- python
summary: Test note
---

# Test Note

This is the content."""
        
        result = parse_markdown(content)
        assert result.frontmatter.summary == "Test note"
        assert "test" in result.frontmatter.tags
        assert "python" in result.frontmatter.tags
        assert result.body.strip().startswith("# Test Note")
    
    def test_parse_markdown_without_frontmatter(self):
        """Test parsing markdown without frontmatter."""
        content = "# Test Note\n\nJust content here."
        
        result = parse_markdown(content)
        assert result.frontmatter.summary == "Note content"
        assert result.body == content
    
    def test_format_markdown(self):
        """Test formatting markdown with frontmatter."""
        frontmatter = NoteFrontmatter(
            created="2025-06-14T10:30:00.000Z",
            updated="2025-06-14T10:30:00.000Z",
            tags=["test"],
            summary="Test note"
        )
        content = "# Test Note\n\nContent here."
        
        result = format_markdown(frontmatter, content)
        
        assert result.startswith("---")
        assert "summary: Test note" in result
        assert "tags:\n- test" in result
        assert "# Test Note" in result
    
    def test_create_default_frontmatter(self):
        """Test creating default frontmatter."""
        title = "Test Note"
        summary = "Test summary"
        tags = ["test", "example"]
        
        result = create_default_frontmatter(title, summary, tags)
        
        assert result.summary == summary
        assert result.tags == tags
        assert result.created is not None
        assert result.updated is not None
    
    def test_extract_title_from_content(self):
        """Test extracting title from markdown content."""
        test_cases = [
            ("# Main Title\n\nContent here", "Main Title"),
            ("## Not a main title\n# This is the title", "This is the title"),
            ("No title here\nJust content", "Untitled Note"),
            ("", "Untitled Note")
        ]
        
        for content, expected in test_cases:
            result = extract_title_from_content(content)
            assert result == expected
    
    def test_kebab_case(self):
        """Test kebab case conversion."""
        test_cases = [
            ("Simple Title", "simple-title"),
            ("Complex Title With Spaces", "complex-title-with-spaces"),
            ("Title-With-Hyphens", "title-with-hyphens"),
            ("Title_With_Underscores", "title-with-underscores"),
            ("Title@With#Special$Characters!", "titlewithspecialcharacters"),
            ("  Spaces  Around  ", "spaces-around")
        ]
        
        for input_text, expected in test_cases:
            result = kebab_case(input_text)
            assert result == expected
    
    def test_generate_filename(self):
        """Test filename generation."""
        title = "Test Note Title"
        date = "2025-06-14"
        
        result = generate_filename(title, date)
        assert result == "test-note-title-2025-06-14.md"
    
    def test_generate_filename_without_date(self):
        """Test filename generation without explicit date."""
        title = "Test Note"
        
        result = generate_filename(title)
        
        assert result.startswith("test-note-")
        assert result.endswith(".md")
        assert len(result.split("-")) >= 4  # title + date parts