import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
import logging

class BaseUITest:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @pytest.fixture(autouse=True)
    def base_setup(self, selenium_driver, mock_services):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.mock_services = mock_services
        self.setup()
    
    def setup(self):
        """Override in subclass to add specific setup"""
        pass
        
    def wait_for_element(self, by, value, timeout=10):
        """Wait for element to be present"""
        return self.wait.until(
            EC.presence_of_element_located((by, value))
        )
    
    def wait_for_clickable(self, by, value, timeout=10):
        """Wait for element to be clickable"""
        return self.wait.until(
            EC.element_to_be_clickable((by, value))
        )
    
    def safe_click(self, by, value, timeout=10):
        """Safely click an element with error handling"""
        try:
            element = self.wait_for_clickable(by, value, timeout)
            element.click()
            return True
        except (TimeoutException, WebDriverException) as e:
            self.logger.error(f"Failed to click element {value}: {str(e)}")
            return False
            
    def safe_send_keys(self, by, value, text, timeout=10):
        """Safely send keys to an element with error handling"""
        try:
            element = self.wait_for_element(by, value, timeout)
            element.clear()
            element.send_keys(text)
            return True
        except (TimeoutException, WebDriverException) as e:
            self.logger.error(f"Failed to send keys to {value}: {str(e)}")
            return False
        