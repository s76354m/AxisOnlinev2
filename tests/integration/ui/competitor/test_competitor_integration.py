"""Integration tests for competitor"""
from tests.ui.base_test import BaseUITest
from selenium.webdriver.common.by import By

class TestCompetitorIntegration(BaseUITest):
    def setup(self):
        self.driver.get("/competitors")
        
    def test_list_operations(self):
        """Test list operations with error handling"""
        # Setup mock data
        self.mock_services.competitor_service.get_all.return_value = [
            {"id": "C1", "name": "Comp1", "status": "Active"},
            {"id": "C2", "name": "Comp2", "status": "Inactive"}
        ]
        
        # Test sorting
        sort_name = self.wait_for_clickable(By.ID, "sort-by-name")
        sort_name.click()
        
        # Verify sort order
        competitors = self.driver.find_elements(By.CLASS_NAME, "competitor-item")
        names = [comp.find_element(By.CLASS_NAME, "name").text for comp in competitors]
        assert names == sorted(names)
        
        # Test filtering
        status_filter = self.driver.find_element(By.ID, "status-filter")
        status_filter.click()
        active_option = self.driver.find_element(By.XPATH, "//option[text()='Active']")
        active_option.click()
        
        # Verify filtered results
        filtered = self.driver.find_elements(By.CLASS_NAME, "competitor-item")
        assert all("Active" in comp.text for comp in filtered)
