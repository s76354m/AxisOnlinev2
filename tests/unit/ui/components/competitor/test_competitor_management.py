import pytest
from unittest.mock import Mock, patch
from app.ui.pages.competitor import render_page
import streamlit as st

@pytest.fixture
def mock_competitor_service():
    with patch('app.services.competitor_service.CompetitorService') as mock_service:
        mock_service.get_all_competitors.return_value = [
            Mock(id=1, name="Competitor A", status="Active"),
            Mock(id=2, name="Competitor B", status="Inactive")
        ]
        yield mock_service

def test_list_view_operations(mock_competitor_service):
    """Test competitor list view operations"""
    # Test sorting
    competitors = mock_competitor_service.get_all_competitors()
    sorted_competitors = sorted(competitors, key=lambda x: x.name)
    assert competitors == sorted_competitors
    
    # Test filtering
    filtered = mock_competitor_service.filter_competitors(status="Active")
    assert all(c.status == "Active" for c in filtered)
    
    # Test search
    search_results = mock_competitor_service.search_competitors("Competitor A")
    assert len(search_results) == 1
    assert search_results[0].name == "Competitor A"

def test_data_operations(mock_competitor_service):
    """Test competitor data operations"""
    # Test add competitor
    new_competitor = {
        "name": "New Competitor",
        "status": "Active",
        "products": ["Product A", "Product B"]
    }
    mock_competitor_service.add_competitor.assert_called_with(new_competitor)
    
    # Test edit competitor
    updated_data = {"status": "Inactive"}
    mock_competitor_service.update_competitor.assert_called_with(1, updated_data)
    
    # Test delete competitor
    mock_competitor_service.delete_competitor.assert_called_with(1)

def test_bulk_operations(mock_competitor_service):
    """Test bulk operations"""
    # Test multiple selection
    selected_ids = [1, 2]
    
    # Test batch processing
    batch_update = {"status": "Inactive"}
    mock_competitor_service.bulk_update.assert_called_with(selected_ids, batch_update)
    
    # Test validation
    validation_result = mock_competitor_service.validate_bulk_update(selected_ids, batch_update)
    assert validation_result.is_valid 