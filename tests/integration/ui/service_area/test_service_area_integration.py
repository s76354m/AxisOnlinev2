"""Integration tests for service_area"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestServiceAreaIntegration:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver, mock_services):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.mock_services = mock_services
        self.driver.get("/service-areas")

    def test_complete_area_selection_workflow(self):
        """Test complete area selection workflow with backend integration"""
        # Reference existing workflow pattern from:
        ```python:tests/e2e/dashboard/test_dashboard_workflow.py
        startLine: 15
        endLine: 31
        ```
        
        # Setup mock data
        self.mock_services.area_service.get_available_areas.return_value = [
            {"id": "A1", "name": "Area 1", "coordinates": [(0,0), (1,1)]},
            {"id": "A2", "name": "Area 2", "coordinates": [(1,1), (2,2)]}
        ]
        
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
        # Setup mock distance calculation
        self.mock_services.area_service.calculate_distance.return_value = 42.5
        
        # Input locations
        origin = self.wait.until(
            EC.presence_of_element_located((By.ID, "origin-point"))
        )
        origin.send_keys("Location A")
        
        dest = self.driver.find_element(By.ID, "destination-point")
        dest.send_keys("Location B")
        
        # Calculate
        self.driver.find_element(By.ID, "calculate-distance").click()
        
        # Verify backend call
        assert self.mock_services.area_service.calculate_distance.called
        assert "42.5" in self.driver.find_element(By.ID, "distance-result").text

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
