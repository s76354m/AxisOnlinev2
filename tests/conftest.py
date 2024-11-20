import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from unittest.mock import Mock
from typing import Generator
from app.db.session import SessionLocal

@pytest.fixture(scope="session")
def driver():
    """Setup WebDriver for tests"""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def base_url():
    """Base URL for Streamlit application"""
    return "http://localhost:8501"

@pytest.fixture(scope="session")
def db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def selenium_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    try:
        yield driver
    finally:
        driver.quit()

@pytest.fixture
def mock_services():
    # Reference implementation from:
    ```python:tests/unit/ui/components/dashboard/test_dashboard_suite.py
    startLine: 7
    endLine: 22
    ```