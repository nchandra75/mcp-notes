"""Tests for date parsing functionality."""

import pytest
from datetime import datetime, timedelta
from mcp_notes.lib.date_parser import parse_natural_date, format_date_for_filename, format_date_for_backlink


class TestDateParser:
    """Test date parsing functionality."""
    
    def test_parse_yesterday(self):
        """Test parsing 'yesterday'."""
        result = parse_natural_date("yesterday")
        expected = datetime.now() - timedelta(days=1)
        
        assert result is not None
        assert result.date() == expected.date()
    
    def test_parse_today(self):
        """Test parsing 'today'."""
        result = parse_natural_date("today")
        expected = datetime.now()
        
        assert result is not None
        assert result.date() == expected.date()
    
    def test_parse_tomorrow(self):
        """Test parsing 'tomorrow'."""
        result = parse_natural_date("tomorrow")
        expected = datetime.now() + timedelta(days=1)
        
        assert result is not None
        assert result.date() == expected.date()
    
    def test_parse_days_ago(self):
        """Test parsing 'X days ago' patterns."""
        test_cases = [
            ("2 days ago", 2),
            ("5 days ago", 5),
            ("1 day ago", 1),
            ("10 days ago", 10)
        ]
        
        for date_str, days_back in test_cases:
            result = parse_natural_date(date_str)
            expected = datetime.now() - timedelta(days=days_back)
            
            assert result is not None
            assert result.date() == expected.date()
    
    def test_parse_weeks_ago(self):
        """Test parsing 'X weeks ago' patterns."""
        test_cases = [
            ("1 week ago", 1),
            ("2 weeks ago", 2),
            ("3 weeks ago", 3)
        ]
        
        for date_str, weeks_back in test_cases:
            result = parse_natural_date(date_str)
            expected = datetime.now() - timedelta(weeks=weeks_back)
            
            assert result is not None
            assert result.date() == expected.date()
    
    def test_parse_last_weekday(self):
        """Test parsing 'last [weekday]' patterns."""
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        
        for weekday in weekdays:
            result = parse_natural_date(f"last {weekday}")
            assert result is not None
            assert result < datetime.now()  # Should be in the past
    
    def test_parse_invalid_date(self):
        """Test parsing invalid date strings."""
        invalid_dates = [
            "invalid nonsense",
            "not a date",
            "",
            None,
            "xyz days ago",
            "last invalidday"
        ]
        
        for invalid_date in invalid_dates:
            result = parse_natural_date(invalid_date)
            assert result is None
    
    def test_format_date_for_filename(self):
        """Test formatting date for filename."""
        test_date = datetime(2025, 6, 14, 15, 30, 45)
        result = format_date_for_filename(test_date)
        assert result == "2025-06-14"
    
    def test_format_date_for_backlink(self):
        """Test formatting date for Obsidian backlink."""
        test_date = datetime(2025, 6, 14, 15, 30, 45)
        result = format_date_for_backlink(test_date)
        assert result == "2025-06-14"