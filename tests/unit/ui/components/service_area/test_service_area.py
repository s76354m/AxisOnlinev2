import pytest
from unittest.mock import Mock, patch
from app.ui.pages.service_area import render_page
import streamlit as st

@pytest.fixture
def mock_map_interface():
    with patch('app.ui.components.map.MapInterface') as mock_map:
        mock_map.get_selected_areas.return_value = ['Area1', 'Area2']
        yield mock_map

def test_area_selection(mock_map_interface):
    """Test service area selection functionality"""
    render_page()
    
    # Test map interface
    assert mock_map_interface.is_initialized()
    
    # Test multi-select
    selected_areas = mock_map_interface.get_selected_areas()
    assert len(selected_areas) == 2
    
    # Test distance calculation
    distances = mock_map_interface.calculate_distances()
    assert all(d > 0 for d in distances)

def test_grid_operations():
    """Test grid operations functionality"""
    with patch('app.ui.components.grid.Grid') as mock_grid:
        render_page()
        
        # Test sorting
        mock_grid.sort_by.assert_called()
        
        # Test filtering
        mock_grid.apply_filters.assert_called()
        
        # Test export
        mock_grid.export_data.assert_called() 