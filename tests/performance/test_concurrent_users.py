"""Load testing with concurrent users"""
import pytest
from concurrent.futures import ThreadPoolExecutor
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def simulate_user_session(user_id):
    """Simulate a single user session"""
    driver = webdriver.Chrome()  # Or configured test browser
    wait = WebDriverWait(driver, 10)
    
    try:
        start_time = time.time()
        driver.get("/service-areas")
        
        # Perform typical user actions
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "grid-row")))
        
        # Apply filters
        filter_button = wait.until(
            EC.element_to_be_clickable((By.ID, "filter-panel-button"))
        )
        filter_button.click()
        
        # Export data
        export_button = wait.until(
            EC.element_to_be_clickable((By.ID, "export-grid"))
        )
        export_button.click()
        
        session_time = time.time() - start_time
        return {
            "user_id": user_id,
            "success": True,
            "session_time": session_time
        }
        
    except Exception as e:
        return {
            "user_id": user_id,
            "success": False,
            "error": str(e)
        }
    finally:
        driver.quit()

def test_concurrent_users():
    """Test system performance with concurrent users"""
    num_users = 10
    max_workers = 5
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(simulate_user_session, range(num_users)))
    
    # Analyze results
    successful_sessions = [r for r in results if r["success"]]
    failed_sessions = [r for r in results if not r["success"]]
    
    avg_session_time = sum(r["session_time"] for r in successful_sessions) / len(successful_sessions)
    
    assert len(successful_sessions) >= num_users * 0.9, "90% of sessions should succeed"
    assert avg_session_time < 10, f"Average session time ({avg_session_time}s) exceeds 10s threshold" 