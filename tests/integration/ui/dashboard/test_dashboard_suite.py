import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestDashboardSuite:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("/dashboard")
        
    def test_summary_metrics(self):
        """Test dashboard summary metrics"""
        # Test load time
        start_time = time.time()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "stMetric")))
        load_time = time.time() - start_time
        assert load_time < 3, f"Load time ({load_time}s) exceeds 3s limit"
        
        # Test data accuracy
        metrics = self.driver.find_elements(By.CLASS_NAME, "stMetric")
        assert len(metrics) == 4, "Should display 4 metrics"
        
        # Test chart rendering
        charts = self.driver.find_elements(By.CLASS_NAME, "stChart")
        assert len(charts) > 0, "Charts should be rendered"
        
    def test_activity_feed(self):
        """Test activity feed functionality"""
        feed = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "activity-feed"))
        )
        
        # Test real-time updates
        initial_items = feed.find_elements(By.CLASS_NAME, "activity-item")
        initial_count = len(initial_items)
        
        # Create new activity and verify update
        self._create_test_activity()
        time.sleep(2)
        
        updated_items = feed.find_elements(By.CLASS_NAME, "activity-item")
        assert len(updated_items) > initial_count
        
    def test_navigation(self):
        """Test navigation functionality"""
        # Test all links
        nav_links = self.driver.find_elements(By.CLASS_NAME, "nav-link")
        for link in nav_links:
            link.click()
            assert self.driver.find_element(By.CLASS_NAME, "breadcrumb")
            
        # Test breadcrumb accuracy
        breadcrumb = self.driver.find_element(By.CLASS_NAME, "breadcrumb")
        assert breadcrumb.text == "Dashboard" 