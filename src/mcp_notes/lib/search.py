"""Search functionality for notes."""

import re
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from .types import SearchResult, NoteFrontmatter
from .markdown import parse_markdown
from .file_manager import FileManager


class SearchEngine:
    """Search engine for notes with relevance scoring."""
    
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
    
    def search_notes(
        self, 
        query: str, 
        limit: int = 10, 
        tags: List[str] = None
    ) -> List[SearchResult]:
        """Search notes with relevance scoring."""
        results = []
        notes = self.file_manager.list_notes()
        
        for filename in notes:
            try:
                content = self.file_manager.read_note(filename)
                parsed = parse_markdown(content)
                
                # Skip notes that don't match tag filter
                if tags and not any(tag in parsed.frontmatter.tags for tag in tags):
                    continue
                
                # Calculate relevance score
                score = self._calculate_relevance(query, parsed, content)
                
                if score > 0:
                    # Extract title from content or use filename
                    title = self._extract_title(content) or filename.replace('.md', '')
                    
                    result = SearchResult(
                        filename=filename,
                        title=title,
                        summary=parsed.frontmatter.summary,
                        relevance_score=score,
                        tags=parsed.frontmatter.tags,
                        created=parsed.frontmatter.created
                    )
                    results.append(result)
                    
            except Exception as e:
                # Skip files that can't be processed
                continue
        
        # Sort by relevance score (descending) and limit results
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:limit]
    
    def _calculate_relevance(self, query: str, parsed: 'ParsedMarkdown', content: str) -> float:
        """Calculate relevance score for a note."""
        score = 0.0
        query_lower = query.lower()
        content_lower = content.lower()
        
        # Title matches (highest weight)
        title = self._extract_title(content)
        if title and query_lower in title.lower():
            score += 10.0
        
        # Summary matches
        if query_lower in parsed.frontmatter.summary.lower():
            score += 5.0
        
        # Tag matches
        for tag in parsed.frontmatter.tags:
            if query_lower in tag.lower():
                score += 3.0
        
        # Content matches (frequency-based)
        content_matches = len(re.findall(re.escape(query_lower), content_lower))
        score += min(content_matches * 0.5, 5.0)  # Cap content score
        
        # Word boundary matches (partial word matching)
        word_pattern = r'\b' + re.escape(query_lower) + r'\b'
        word_matches = len(re.findall(word_pattern, content_lower))
        score += word_matches * 1.0
        
        return score
    
    def _extract_title(self, content: str) -> str:
        """Extract title from markdown content."""
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()
        return ""
    
    def get_notes_by_tags(self, tags: List[str]) -> List[Dict[str, Any]]:
        """Get all notes that match any of the given tags."""
        results = []
        notes = self.file_manager.list_notes()
        
        for filename in notes:
            try:
                content = self.file_manager.read_note(filename)
                parsed = parse_markdown(content)
                
                # Check if note has any matching tags
                if any(tag in parsed.frontmatter.tags for tag in tags):
                    title = self._extract_title(content) or filename.replace('.md', '')
                    
                    results.append({
                        'filename': filename,
                        'title': title,
                        'summary': parsed.frontmatter.summary,
                        'tags': parsed.frontmatter.tags,
                        'created': parsed.frontmatter.created,
                        'updated': parsed.frontmatter.updated
                    })
            except Exception:
                continue
        
        # Sort by creation date (newest first)
        results.sort(key=lambda x: x['created'], reverse=True)
        return results