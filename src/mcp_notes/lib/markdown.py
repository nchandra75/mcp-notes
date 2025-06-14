"""Markdown handling utilities."""

import re
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

import yaml

from .types import NoteFrontmatter


class ParsedMarkdown:
    """Parsed markdown with frontmatter and body."""
    
    def __init__(self, frontmatter: NoteFrontmatter, body: str):
        self.frontmatter = frontmatter
        self.body = body


def parse_markdown(content: str) -> ParsedMarkdown:
    """Parse markdown content with YAML frontmatter."""
    # Match frontmatter pattern: ---\n...yaml...\n---
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(frontmatter_pattern, content, re.DOTALL)
    
    if not match:
        # No frontmatter found, create default
        frontmatter_data = {
            'created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat(),
            'tags': [],
            'summary': 'Note content'
        }
        frontmatter = NoteFrontmatter(**frontmatter_data)
        return ParsedMarkdown(frontmatter, content)
    
    yaml_content = match.group(1)
    body_content = match.group(2)
    
    try:
        frontmatter_data = yaml.safe_load(yaml_content) or {}
        frontmatter = NoteFrontmatter(**frontmatter_data)
        return ParsedMarkdown(frontmatter, body_content)
    except Exception as e:
        # If YAML parsing fails, treat as regular content
        frontmatter_data = {
            'created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat(),
            'tags': [],
            'summary': 'Note content'
        }
        frontmatter = NoteFrontmatter(**frontmatter_data)
        return ParsedMarkdown(frontmatter, content)


def format_markdown(frontmatter: NoteFrontmatter, content: str) -> str:
    """Format markdown with YAML frontmatter."""
    # Convert frontmatter to dict, excluding None values
    frontmatter_dict = frontmatter.model_dump(exclude_none=True)
    
    # Format YAML
    yaml_content = yaml.dump(frontmatter_dict, default_flow_style=False, sort_keys=False)
    
    return f"""---
{yaml_content.strip()}
---

{content}"""


def create_default_frontmatter(
    title: str,
    summary: Optional[str] = None,
    tags: Optional[List[str]] = None,
    conversation_id: Optional[str] = None,
    ai_client: Optional[str] = None,
) -> NoteFrontmatter:
    """Create default frontmatter for a new note."""
    now = datetime.now().isoformat()
    
    frontmatter_data = {
        'created': now,
        'updated': now,
        'tags': tags or [],
        'summary': summary or f"Note about {title}",
    }
    
    # Only add optional fields if they have non-empty values
    if conversation_id and conversation_id.strip():
        frontmatter_data['conversation_id'] = conversation_id
    if ai_client and ai_client.strip():
        frontmatter_data['ai_client'] = ai_client
    
    return NoteFrontmatter(**frontmatter_data)


def extract_title_from_content(content: str) -> str:
    """Extract title from markdown content (first heading)."""
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    return "Untitled Note"


def kebab_case(text: str) -> str:
    """Convert text to kebab-case for filenames."""
    # Remove special characters and convert to lowercase
    text = re.sub(r'[^\w\s-]', '', text.lower())
    # Replace spaces and underscores with hyphens
    text = re.sub(r'[\s_]+', '-', text)
    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)
    # Remove leading/trailing hyphens
    return text.strip('-')


def generate_filename(title: str, date: Optional[str] = None) -> str:
    """Generate a kebab-case filename from title and date."""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    kebab_title = kebab_case(title)
    return f"{kebab_title}-{date}.md"