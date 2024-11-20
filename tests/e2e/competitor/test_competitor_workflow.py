"""E2E tests for competitor workflow"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestCompetitorDataOperations:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("/competitors")

    def test_add_competitor(self):
        """Test adding a new competitor"""
        # Click Add Competitor button
        add_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "add-competitor-btn"))
        )
        add_button.click()

        # Fill form
        self.driver.find_element(By.ID, "competitor-name").send_keys("Test Competitor")
        self.driver.find_element(By.ID, "competitor-code").send_keys("COMP001")
        self.driver.find_element(By.ID, "market-share").send_keys("15.5")
        
        # Submit form
        self.driver.find_element(By.ID, "submit-competitor").click()
        
        # Verify success
        success_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        assert "Competitor added successfully" in success_message.text

    def test_edit_competitor(self):
        """Test editing an existing competitor"""
        # Reference existing functional test structure from:
        ```python:tests/e2e/ui/run_functional_tests.py
        startLine: 39
        endLine: 51
        ```
        
        # Additional edit verification
        edited_name = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "competitor-name"))
        )
        assert edited_name.text == "Updated Competitor Name"

    def test_bulk_operations(self):
        """Test bulk competitor operations"""
        # Select multiple competitors
        checkboxes = self.driver.find_elements(By.CLASS_NAME, "competitor-select")
        for checkbox in checkboxes[:2]:
            checkbox.click()
        
        # Perform bulk action
        self.driver.find_element(By.ID, "bulk-action-select").click()
        self.driver.find_element(By.XPATH, "//option[text()='Deactivate']").click()
        self.driver.find_element(By.ID, "apply-bulk-action").click()
        
        # Verify bulk update
        success_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        assert "competitors updated" in success_message.text

"""E2E tests for competitor list view"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestCompetitorListView:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("/competitors")
        
    def test_sorting_functionality(self):
        """Test sorting of competitor list"""
        # Reference sorting pattern from dashboard workflow:
        ```python:tests/e2e/dashboard/test_dashboard_workflow.py
        startLine: 96
        endLine: 113
        ```
        
        # Test different sort columns
        sort_columns = ["name", "status", "market-share"]
        for column in sort_columns:
            sort_header = self.wait.until(
                EC.element_to_be_clickable((By.ID, f"sort-{column}"))
            )
            sort_header.click()
            time.sleep(0.5)  # Allow for sorting
            
            # Verify sort indicator
            assert "sorted" in sort_header.get_attribute("class")
    
    def test_filtering_functionality(self):
        """Test filtering of competitors"""
        # Open filter panel
        filter_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "filter-panel-button"))
        )
        filter_button.click()
        
        # Apply multiple filters
        filters = {
            "status": "Active",
            "market-share": ">10",
            "region": "North"
        }
        
        for filter_key, filter_value in filters.items():
            filter_input = self.driver.find_element(By.ID, f"filter-{filter_key}")
            filter_input.clear()
            filter_input.send_keys(filter_value)
        
        # Apply filters
        self.driver.find_element(By.ID, "apply-filters").click()
        
        # Verify filtered results
        results = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "competitor-row"))
        )
        
        # Verify filter application
        for result in results:
            status = result.find_element(By.CLASS_NAME, "status-cell").text
            market_share = float(result.find_element(By.CLASS_NAME, "market-share-cell").text)
            region = result.find_element(By.CLASS_NAME, "region-cell").text
            
            assert status == "Active"
            assert market_share > 10
            assert region == "North"
    
    def test_search_functionality(self):
        """Test search with different criteria"""
        search_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "competitor-search"))
        )
        
        search_terms = ["Test Corp", "12345", "Healthcare"]
        for term in search_terms:
            # Clear previous search
            search_input.clear()
            search_input.send_keys(term)
            time.sleep(0.5)  # Allow for search debounce
            
            # Verify search results
            results = self.driver.find_elements(By.CLASS_NAME, "competitor-row")
            if results:
                for result in results:
                    assert term.lower() in result.text.lower()
            else:
                no_results = self.driver.find_element(By.CLASS_NAME, "no-results-message")
                assert "No competitors found" in no_results.text
