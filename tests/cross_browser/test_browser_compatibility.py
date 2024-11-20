"""Cross-browser compatibility test suite"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestBrowserCompatibility:
    @pytest.fixture(params=["chrome", "firefox"])
    def browser(self, request):
        if request.param == "chrome":
            driver = webdriver.Chrome()
        else:
            driver = webdriver.Firefox()
            
        driver.set_window_size(1920, 1080)
        yield driver
        driver.quit()

    def test_service_area_compatibility(self, browser):
        """Test service area functionality across browsers"""
        wait = WebDriverWait(browser, 10)
        browser.get("/service-areas")
        
        # Test map rendering
        map_element = wait.until(
            EC.presence_of_element_located((By.ID, "service-area-map"))
        )
        assert map_element.is_displayed()