"""E2E tests for service area workflow"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestServiceAreaSelection:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("/service-areas")

    def test_map_interface(self):
        """Test map interface functionality"""
        # Reference existing test pattern from:
        ```python:tests/e2e/ui/run_functional_tests.py
        startLine: 25
        endLine: 37
        ```
        
        # Wait for map to load
        map_element = self.wait.until(
            EC.presence_of_element_located((By.ID, "service-area-map"))
        )
        assert map_element.is_displayed()
        
        # Test map controls
        zoom_in = self.driver.find_element(By.CLASS_NAME, "map-zoom-in")
        zoom_in.click()
        
        # Select area on map
        map_area = self.driver.find_element(By.CLASS_NAME, "map-selectable-area")
        map_area.click()
        
        # Verify area selection
        selected_area = self.driver.find_element(By.CLASS_NAME, "selected-area")
        assert selected_area.is_displayed()

    def test_multi_select_functionality(self):
        """Test multi-select area functionality"""
        # Open area selection panel
        select_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "area-select-btn"))
        )
        select_button.click()
        
        # Select multiple areas
        area_checkboxes = self.driver.find_elements(By.CLASS_NAME, "area-checkbox")
        selected_areas = area_checkboxes[:3]  # Select first 3 areas
        
        for area in selected_areas:
            area.click()
            time.sleep(0.2)  # Allow for selection update
        
        # Verify selections
        selected_count = len(self.driver.find_elements(By.CLASS_NAME, "selected-area"))
        assert selected_count == 3
        
        # Verify summary panel
        summary = self.driver.find_element(By.ID, "selection-summary")
        assert "3 areas selected" in summary.text

    def test_distance_calculations(self):
        """Test distance calculation functionality"""
        # Select origin point
        origin_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "origin-point"))
        )
        origin_input.send_keys("Test Location A")
        
        # Select destination
        dest_input = self.driver.find_element(By.ID, "destination-point")
        dest_input.send_keys("Test Location B")
        
        # Calculate distance
        calc_button = self.driver.find_element(By.ID, "calculate-distance")
        calc_button.click()
        
        # Verify calculation results
        distance_result = self.wait.until(
            EC.presence_of_element_located((By.ID, "distance-result"))
        )
        
        assert "Distance:" in distance_result.text
        assert "miles" in distance_result.text
        
        # Verify calculation accuracy
        distance_value = float(distance_result.text.split()[1])
        assert 0 < distance_value < 1000  # Reasonable distance range

    def test_map_interface_errors(self):
        """Test map interface error handling"""
        # Test offline map handling
        self.driver.execute_script("window.localStorage.setItem('mock_map_offline', 'true')")
        self.driver.refresh()
        
        error_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "map-error"))
        )
        assert "Map service unavailable" in error_message.text
        
        # Clear mock offline state
        self.driver.execute_script("window.localStorage.removeItem('mock_map_offline')")
        
    def test_multi_select_edge_cases(self):
        """Test multi-select edge cases"""
        # Test maximum selection limit
        select_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "area-select-btn"))
        )
        select_button.click()
        
        # Try to select more than maximum allowed
        area_checkboxes = self.driver.find_elements(By.CLASS_NAME, "area-checkbox")
        max_selections = 10
        
        for area in area_checkboxes[:max_selections + 1]:
            area.click()
            time.sleep(0.2)
        
        # Verify warning message
        warning = self.driver.find_element(By.CLASS_NAME, "selection-warning")
        assert "Maximum 10 areas allowed" in warning.text
        
        # Verify only max selections were made
        selected_count = len(self.driver.find_elements(By.CLASS_NAME, "selected-area"))
        assert selected_count == max_selections
        
    def test_distance_calculation_validation(self):
        """Test distance calculation validation"""
        # Test invalid location input
        origin_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "origin-point"))
        )
        origin_input.send_keys("Invalid Location XYZ")
        
        calc_button = self.driver.find_element(By.ID, "calculate-distance")
        calc_button.click()
        
        # Verify validation message
        validation_error = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "validation-error"))
        )
        assert "Location not found" in validation_error.text

    def test_area_selection_error_handling(self):
        """Test area selection error scenarios"""
        # Network failure simulation
        self.driver.execute_script(
            "window.localStorage.setItem('mock_network_error', 'true')"
        )
        
        select_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "area-select-btn"))
        )
        select_button.click()
        
        # Verify error message
        error_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "network-error"))
        )
        assert "Unable to load areas" in error_message.text
        
        # Test retry functionality
        retry_button = self.driver.find_element(By.ID, "retry-load")
        retry_button.click()
        
        # Clear mock error
        self.driver.execute_script(
            "window.localStorage.removeItem('mock_network_error')"
        )
        
        # Verify recovery
        area_list = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "area-item"))
        )
        assert len(area_list) > 0

class TestServiceAreaGridOperations:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("/service-areas/grid")
        
    def test_grid_sorting(self):
        """Test grid sorting functionality"""
        # Reference competitor sorting pattern:
        ```python:tests/e2e/competitor/test_competitor_workflow.py
        startLine: 14
        endLine: 34
        ```
        
        sort_columns = ["area_name", "zip_code", "distance"]
        for column in sort_columns:
            sort_header = self.wait.until(
                EC.element_to_be_clickable((By.ID, f"sort-{column}"))
            )
            sort_header.click()
            time.sleep(0.5)
            
            # Verify sort indicator
            assert "sorted" in sort_header.get_attribute("class")
            
            # Verify sort order
            column_values = [elem.text for elem in 
                           self.driver.find_elements(By.CLASS_NAME, f"{column}-cell")]
            assert column_values == sorted(column_values)
            
    def test_grid_filtering(self):
        """Test grid filtering functionality"""
        # Open filter panel
        filter_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "filter-panel-button"))
        )
        filter_button.click()
        
        # Apply filters
        filters = {
            "zip_code": "12345",
            "distance": "<50",
            "status": "Active"
        }
        
        for filter_key, filter_value in filters.items():
            filter_input = self.driver.find_element(By.ID, f"filter-{filter_key}")
            filter_input.clear()
            filter_input.send_keys(filter_value)
            
        self.driver.find_element(By.ID, "apply-filters").click()
        
        # Verify filtered results
        grid_rows = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "grid-row"))
        )
        
        for row in grid_rows:
            zip_code = row.find_element(By.CLASS_NAME, "zip_code-cell").text
            distance = float(row.find_element(By.CLASS_NAME, "distance-cell").text)
            status = row.find_element(By.CLASS_NAME, "status-cell").text
            
            assert "12345" in zip_code
            assert distance < 50
            assert status == "Active"
            
    def test_grid_export(self):
        """Test grid export functionality"""
        # Click export button
        export_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "export-grid"))
        )
        export_button.click()
        
        # Select export format
        format_select = self.driver.find_element(By.ID, "export-format")
        format_select.click()
        self.driver.find_element(By.XPATH, "//option[text()='CSV']").click()
        
        # Trigger export
        self.driver.find_element(By.ID, "confirm-export").click()
        
        # Verify export success
        success_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "export-success"))
        )
        assert "Export completed successfully" in success_message.text

    def test_grid_export_functionality(self):
        """Test grid export functionality"""
        # Setup export button
        export_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "export-grid"))
        )
        export_button.click()
        
        # Select export format
        format_select = self.driver.find_element(By.ID, "export-format")
        format_select.click()
        
        # Test CSV export
        csv_option = self.driver.find_element(By.XPATH, "//option[@value='csv']")
        csv_option.click()
        
        # Trigger export
        self.driver.find_element(By.ID, "confirm-export").click()
        
        # Verify export success
        success_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "export-success"))
        )
        assert "Export completed" in success_message.text

    def test_grid_error_handling(self):
        """Test grid error handling"""
        # Reference error handling pattern from:
        ```python:tests/e2e/dashboard/test_dashboard_workflow.py
        startLine: 58
        endLine: 74
        ```
        
        # Test data load error
        self.driver.execute_script(
            "window.localStorage.setItem('mock_grid_error', 'true')"
        )
        self.driver.refresh()
        
        # Verify error message
        error_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "grid-error"))
        )
        assert "Unable to load grid data" in error_message.text
        
        # Test retry functionality
        retry_button = self.driver.find_element(By.ID, "retry-load")
        retry_button.click()
        
        # Verify recovery
        grid_rows = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "grid-row"))
        )
        assert len(grid_rows) > 0

class TestServiceAreaDistance:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver, mock_services):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.mock_services = mock_services
        self.driver.get("/service-areas/distance")

    def test_distance_calculation(self):
        """Test distance calculation functionality"""
        # Reference pattern from:
        ```python:tests/e2e/service_area/test_service_area_workflow.py
        startLine: 41
        endLine: 63
        ```
        
        # Select origin point
        origin_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "origin-point"))
        )
        origin_input.send_keys("12345")  # ZIP code
        
        # Select destination areas
        area_checkboxes = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "area-checkbox"))
        )
        area_checkboxes[0].click()
        area_checkboxes[1].click()
        
        # Calculate distances
        calculate_button = self.driver.find_element(By.ID, "calculate-distance")
        calculate_button.click()
        
        # Verify results
        distance_results = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "distance-result"))
        )
        assert len(distance_results) == 2
        
        # Verify distance format
        for result in distance_results:
            distance_value = result.find_element(By.CLASS_NAME, "distance-value").text
            assert "miles" in distance_value
            assert float(distance_value.split()[0]) > 0

    def test_distance_calculation_error_handling(self):
        """Test distance calculation error scenarios"""
        # Reference pattern from:
        ```python:tests/e2e/dashboard/test_dashboard_workflow.py
        startLine: 58
        endLine: 74
        ```
        
        # Invalid ZIP code
        origin_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "origin-point"))
        )
        origin_input.send_keys("invalid")
        
        calculate_button = self.driver.find_element(By.ID, "calculate-distance")
        calculate_button.click()
        
        # Verify error message
        error_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "validation-error"))
        )
        assert "Invalid ZIP code format" in error_message.text
        
        # Test API error
        self.mock_services.distance_service.calculate.side_effect = Exception("API Error")
        
        origin_input.clear()
        origin_input.send_keys("12345")
        calculate_button.click()
        
        # Verify error handling
        api_error = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "api-error"))
        )
        assert "Unable to calculate distance" in api_error.text
