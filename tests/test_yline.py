"""Test Y-Line functionality"""
import pytest
from datetime import datetime
from app.models.yline import YLineItem, YLineManager
from unittest.mock import MagicMock

def test_yline_item_creation(mock_db):
    """Test Y-Line item creation"""
    # Arrange
    item = YLineItem(
        ipa_number="IPA001",
        product_code="A1",
        description="Test Product",
        pre_award=True,
        post_award=False,
        status="Active",
        last_updated=datetime.now(),
        notes="Test notes"
    )
    manager = YLineManager(mock_db)
    
    # Configure mock
    mock_result = MagicMock()
    mock_result.ProductCode = "A1"
    mock_db.execute.return_value.fetchone.return_value = mock_result
    
    # Act
    manager.create_yline_item(item)
    
    # Assert
    result = mock_db.execute(
        "SELECT * FROM CS_EXP_YLine WHERE IPA_Number = ?",
        ("IPA001",)
    ).fetchone()
    assert result.ProductCode == "A1"

def test_yline_filtering(mock_db):
    """Test Y-Line item filtering"""
    # Arrange
    manager = YLineManager(mock_db)
    items = [
        YLineItem("IPA001", "A1", "Test 1", True, False, "Active", datetime.now()),
        YLineItem("IPA002", "A2", "Test 2", False, True, "Inactive", datetime.now())
    ]
    for item in items:
        manager.create_yline_item(item)
    
    # Act
    active_items = manager.get_yline_items(status_filter="Active")
    
    # Assert
    assert len(active_items) == 1
    assert active_items.iloc[0]['IPA_Number'] == "IPA001"

def test_yline_validation():
    """Test Y-Line validation rules"""
    # Arrange
    item = YLineItem(
        ipa_number="IPA001",
        product_code="A1",
        description="Test Product",
        pre_award=True,
        post_award=True,  # Should raise validation error
        status="Active",
        last_updated=datetime.now()
    )
    
    # Act & Assert
    with pytest.raises(ValueError):
        validate_yline_item(item) 