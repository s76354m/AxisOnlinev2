"""Integration tests for dashboard"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.ui.pages.dashboard import render_page
import time

@pytest.fixture
def dashboard_page(selenium_driver):
    """Setup dashboard page for testing"""
    selenium_driver.get("/dashboard")
    return selenium_driver

def test_dashboard_load_time(dashboard_page):
    """Test dashboard load time is under 3 seconds"""
    start_time = time.time()
    WebDriverWait(dashboard_page, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    load_time = time.time() - start_time
    assert load_time < 3, f"Dashboard load time ({load_time}s) exceeds 3s threshold"

def test_metrics_accuracy(dashboard_page, mock_services):
    """Test dashboard metrics accuracy"""
    # Setup mock data
    mock_services.project_service.get_all_projects.return_value = [
        {"Status": "Active"}, {"Status": "Active"}, {"Status": "Completed"}
    ]
    
    # Verify metrics
    metrics = dashboard_page.find_elements(By.CLASS_NAME, "stMetric")
    assert len(metrics) == 4, "Should display 4 metrics"
    assert "Total Projects: 3" in metrics[0].text
    assert "Active Projects: 2" in metrics[1].text

def test_database_status(dashboard_page):
    """Test database status display"""
    status_element = dashboard_page.find_element(By.CLASS_NAME, "stSuccess")
    assert "Database connection successful" in status_element.text

def test_chart_rendering(dashboard_page):
    """Test chart rendering"""
    WebDriverWait(dashboard_page, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "js-plotly-plot"))
    )
    charts = dashboard_page.find_elements(By.CLASS_NAME, "js-plotly-plot")
    assert len(charts) > 0, "Charts should be rendered"
