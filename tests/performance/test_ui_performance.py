import pytest
import time
from app.utils.performance_monitor import PerformanceMonitor

def test_ui_response_times():
    """Test UI component response times"""
    monitor = PerformanceMonitor()
    
    # Test dashboard load time
    with monitor.measure('dashboard_load'):
        render_dashboard_page()
    assert monitor.get_metric('dashboard_load') < 3000  # 3s limit
    
    # Test navigation response
    with monitor.measure('navigation'):
        navigate_to_page('Projects')
    assert monitor.get_metric('navigation') < 500  # 500ms limit
    
    # Test form interactions
    with monitor.measure('form_submit'):
        submit_test_form()
    assert monitor.get_metric('form_submit') < 1000  # 1s limit 