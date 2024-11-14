"""Test database operations"""
import pytest
from app.utils.db_monitor import (
    DatabaseMonitor,
    verify_database_connection,
    verify_table_integrity
)

def test_database_monitor(mock_db):
    """Test database monitoring"""
    # Arrange
    monitor = DatabaseMonitor()
    
    # Act
    monitor.log_operation('TEST', 'SUCCESS')
    monitor.log_error('TEST', Exception('Test error'))
    
    # Assert
    stats = monitor.get_stats()
    assert stats['operations'] == 1
    assert stats['errors'] == 1

def test_database_connection(mock_db):
    """Test database connection verification"""
    # Act
    result = verify_database_connection(mock_db)
    
    # Assert
    assert result is True

def test_table_integrity(mock_db):
    """Test table integrity check"""
    # Act
    result = verify_table_integrity()
    
    # Assert
    assert not result.empty
    assert 'CS_EXP_Project_Translation' in result['table'].values 