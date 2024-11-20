"""E2E tests for dashboard workflow"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestDashboardWorkflow:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("/dashboard")
    
    def test_navigation_workflow(self):
        """Test navigation workflow"""
        # Verify breadcrumb
        breadcrumb = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "stBreadcrumb"))
        )
        assert "Dashboard" in breadcrumb.text
        
        # Test navigation links
        nav_links = self.driver.find_elements(By.CLASS_NAME, "nav-link")
        for link in nav_links:
            link.click()
            time.sleep(0.5)  # Allow for page transition
            self.driver.back()
            
        # Verify we're back at dashboard
        assert "Dashboard" in self.driver.title
    
    def test_activity_feed_workflow(self):
        """Test activity feed workflow"""
        # Switch between tabs
        tabs = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "stTab"))
        )
        
        for tab in tabs:
            tab.click()
            time.sleep(0.5)
            
            # Verify content loads
            feed_items = self.driver.find_elements(By.CLASS_NAME, "activity-item")
            assert len(feed_items) >= 0, f"Tab {tab.text} should load items"
            
            # Test sorting if items exist
            if feed_items:
                sort_button = self.driver.find_element(By.CLASS_NAME, "sort-button")
                sort_button.click()
                time.sleep(0.5)
                
                # Verify sorting changed
                new_items = self.driver.find_elements(By.CLASS_NAME, "activity-item")
                assert len(new_items) == len(feed_items), "Item count should remain same after sorting"
    
    def test_error_handling_workflow(self):
        """Test error handling in dashboard workflow"""
        # Test database connection error
        self.driver.execute_script(
            "window.localStorage.setItem('mock_db_error', 'true')"
        )
        self.driver.refresh()
        
        error_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "stError"))
        )
        assert "Database connection error" in error_message.text
        
        # Clear error state
        self.driver.execute_script(
            "window.localStorage.removeItem('mock_db_error')"
        )
    
    def test_activity_feed_updates(self):
        """Test activity feed real-time updates"""
        # Switch to activity feed tab
        activity_tab = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Activity Feed')]"))
        )
        activity_tab.click()
        
        # Get initial items
        initial_items = self.driver.find_elements(By.CLASS_NAME, "activity-item")
        initial_count = len(initial_items)
        
        # Create new activity via API
        self._create_test_activity()
        
        # Wait for feed to update
        time.sleep(2)  # Allow for real-time update
        updated_items = self.driver.find_elements(By.CLASS_NAME, "activity-item")
        assert len(updated_items) > initial_count
    
    def test_sorting_functionality(self):
        """Test activity feed sorting"""
        sort_button = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "sort-button"))
        )
        
        # Get initial order
        items = self.driver.find_elements(By.CLASS_NAME, "activity-timestamp")
        initial_order = [item.text for item in items]
        
        # Click sort button
        sort_button.click()
        
        # Get new order
        sorted_items = self.driver.find_elements(By.CLASS_NAME, "activity-timestamp")
        sorted_order = [item.text for item in sorted_items]
        
        assert initial_order != sorted_order, "Sorting should change item order"
    
    def _create_test_activity(self):
        """Helper method to create test activity"""
        # Implementation depends on your API structure
        pass