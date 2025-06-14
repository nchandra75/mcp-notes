"""Pytest configuration and fixtures."""

import os
import pytest
import tempfile
import shutil
from pathlib import Path
import subprocess
import sys

# Add src to path so we can import our modules
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from mcp_notes.main import MCPNotesServer


@pytest.fixture
def temp_vault():
    """Create a temporary vault directory for testing."""
    temp_dir = tempfile.mkdtemp(prefix="mcp_notes_test_")
    vault_path = Path(temp_dir) / "test-vault"
    vault_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize git repository
    subprocess.run(["git", "init"], cwd=vault_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=vault_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=vault_path, check=True)
    
    # Set environment variable
    old_vault_path = os.environ.get("OBSIDIAN_VAULT_PATH")
    os.environ["OBSIDIAN_VAULT_PATH"] = str(vault_path)
    
    yield str(vault_path)
    
    # Cleanup
    if old_vault_path:
        os.environ["OBSIDIAN_VAULT_PATH"] = old_vault_path
    else:
        os.environ.pop("OBSIDIAN_VAULT_PATH", None)
    
    shutil.rmtree(temp_dir)


@pytest.fixture
def mcp_server(temp_vault):
    """Create an MCP server instance for testing."""
    return MCPNotesServer(temp_vault)


@pytest.fixture
def sample_note_params():
    """Sample parameters for creating a note."""
    return {
        "title": "Test Note",
        "content": "# Test Note\n\nThis is a test note with some content.",
        "summary": "A test note for validation",
        "tags": ["test", "sample"],
        "conversation_id": "test_conv_001",
        "ai_client": "test-client"
    }