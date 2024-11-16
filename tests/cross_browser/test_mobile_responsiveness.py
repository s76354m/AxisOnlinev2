"""Mobile responsiveness test suite"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestMobileResponsiveness:
    @pytest.fixture(params=[
        ("iPhone 12", 390, 844),
        ("iPhone SE", 375, 667),
        ("iPad Air", 820, 1180),
        ("Galaxy S21", 360, 800),
        ("Pixel 6", 393, 851)
    ])
    def mobile_device(self, request, selenium_driver):
        device_name, width, height = request.param
        selenium_driver.set_window_size(width, height)
        return selenium_driver, device_name, width, height

    def test_responsive_layout(self, mobile_device):
        """Test responsive layout across different mobile devices"""
        driver, device_name, width, height = mobile_device
        wait = WebDriverWait(driver, 10)
        
        # Reference pattern from:
        ```python:tests/e2e/service_area/test_service_area_workflow.py
        startLine: 15
        endLine: 39
        ```
        
        # Test critical pages
        test_pages = [
            "/dashboard",
            "/service-areas",
            "/y-line/awards",
            "/notes"
        ]
        
        for page in test_pages:
            driver.get(page)
            
            # Verify mobile navigation
            hamburger_menu = wait.until(
                EC.presence_of_element_located((By.ID, "mobile-menu"))
            )
            assert hamburger_menu.is_displayed()
            
            # Test menu functionality
            hamburger_menu.click()
            nav_menu = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "mobile-nav"))
            )
            assert nav_menu.is_displayed()
            
            # Verify content width
            main_content = driver.find_element(By.ID, "main-content")
            content_width = main_content.get_property("offsetWidth")
            assert content_width <= width, f"Content width ({content_width}) exceeds device width ({width})"
            
            # Test touch interactions
            if "service-areas" in page:
                map_element = driver.find_element(By.ID, "service-area-map")
                driver.execute_script("""
                    arguments[0].dispatchEvent(new TouchEvent('touchstart', {
                        bubbles: true
                    }));
                """, map_element)
                
                # Verify touch event handling
                assert "touch-active" in map_element.get_attribute("class")

Would you like me to:
1. Add more mobile-specific test cases
2. Move on to implementing the Security Testing Suite
3. Start on Notes System tests

Which would you prefer? 