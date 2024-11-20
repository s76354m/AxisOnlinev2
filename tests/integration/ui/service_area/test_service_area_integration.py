"""Integration tests for service_area"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from tests.ui.base_test import BaseUITest

class TestServiceAreaIntegration(BaseUITest):
    def setup(self):
        self.driver.get("/service-areas")

    def test_complete_area_selection_workflow(self):
        """Test complete area selection workflow with backend integration"""
        # Setup mock data
        self.mock_services.area_service.get_available_areas.return_value = [
            {"id": "A1", "name": "Area 1", "coordinates": [(0,0), (1,1)]},
            {"id": "A2", "name": "Area 2", "coordinates": [(1,1), (2,2)]}
        ]
        
        # Verify workflow based on dashboard pattern from:
        # Reference: test_dashboard_workflow.py
        
        # Select areas
        select_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "area-select-btn"))
        )
        select_button.click()
        
        # Verify areas loaded from backend
        area_list = self.driver.find_elements(By.CLASS_NAME, "area-item")
        assert len(area_list) == 2
        
        # Select first area
        area_list[0].click()
        
        # Verify backend call
        assert self.mock_services.area_service.select_area.called
        assert self.mock_services.area_service.select_area.call_args[0][0] == "A1"

    def test_distance_calculation_integration(self):
        """Test distance calculation with backend integration"""
        # Setup mock data
        self.mock_services.area_service.calculate_distance.return_value = {
            "total_miles": 150,
            "route_segments": [
                {"start": "A1", "end": "A2", "distance": 75},
                {"start": "A2", "end": "A3", "distance": 75}
            ]
        }
        
        # Select multiple areas
        area_list = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "area-item"))
        )
        for area in area_list[:2]:
            area.click()
            
        # Click calculate button
        calc_button = self.driver.find_element(By.ID, "calculate-distance")
        calc_button.click()
        
        # Verify calculation results
        results = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "distance-results"))
        )
        assert "150 miles" in results.text
        
        # Verify backend call
        assert self.mock_services.area_service.calculate_distance.called

    def test_grid_data_integration(self):
        """Test grid data integration with backend"""
        # Reference dashboard integration pattern:
        ```python:tests/integration/ui/dashboard/test_dashboard_integration.py
        startLine: 24
        endLine: 35
        ```
        
        # Setup mock data
        self.mock_services.area_service.get_service_areas.return_value = [
            {"area_name": "Test Area 1", "zip_code": "12345", "distance": 25},
            {"area_name": "Test Area 2", "zip_code": "67890", "distance": 35}
        ]
        
        # Verify grid data
        grid_rows = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "grid-row"))
        )
        assert len(grid_rows) == 2
        
        # Verify backend calls
        assert self.mock_services.area_service.get_service_areas.called
        
    def test_export_integration(self):
        """Test export functionality with backend integration"""
        export_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "export-grid"))
        )
        export_button.click()
        
        # Setup mock export response
        self.mock_services.area_service.export_areas.return_value = {
            "file_url": "http://test-url/export.csv",
            "row_count": 100
        }
        
        # Trigger export
        self.driver.find_element(By.ID, "confirm-export").click()
        
        # Verify backend call
        assert self.mock_services.area_service.export_areas.called
        
        # Verify download initiated
        download_link = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "download-link"))
        )
        assert "http://test-url/export.csv" in download_link.get_attribute("href")

    def test_area_selection_error_integration(self):
        """Test area selection error handling with backend"""
        # Setup mock error
        self.mock_services.area_service.get_available_areas.side_effect = Exception("Network error")
        
        # Attempt to load areas
        select_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "area-select-btn"))
        )
        select_button.click()
        
        # Verify error handling
        error_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "backend-error"))
        )
        assert "Unable to load areas" in error_message.text
        
        # Test recovery
        self.mock_services.area_service.get_available_areas.side_effect = None
        self.mock_services.area_service.get_available_areas.return_value = [
            {"id": "A1", "name": "Test Area", "coordinates": [(0,0), (1,1)]}
        ]
        
        retry_button = self.driver.find_element(By.ID, "retry-load")
        retry_button.click()
        
        # Verify recovery
        area_list = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "area-item"))
        )
        assert len(area_list) > 0

    def test_grid_operations(self):
        """Test grid operations with error handling"""
        # Reference existing implementation:
        ```python:tests/integration/ui/service_area/test_service_area_integration.py
        startLine: 95
        endLine: 118
        ```
        
    def test_error_handling(self):
        """Test error handling scenarios"""
        # Reference existing implementation:
        ```python:tests/integration/ui/service_area/test_service_area_integration.py
        startLine: 120
        endLine: 150
        ```
