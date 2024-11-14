"""Test database monitoring"""
import pytest
from unittest.mock import MagicMock
from app.utils.db_monitor import verify_database_connection

def test_database_connection_failure():
    """Test database connection failure"""
    # Arrange
    mock_db = MagicMock()
    mock_db.execute.side_effect = Exception("Connection failed")
    
    # Act
    result = verify_database_connection(mock_db)
    
    # Assert
    assert result is False 