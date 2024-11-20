import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BaseUITest:
    @pytest.fixture(autouse=True)
    def setup_ui(self, selenium_driver):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.setup()
    
    def setup(self):
        """Override in subclass to add specific setup"""
        pass 