import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def verify_ui_components():
    """Verify all UI components"""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 10)
    base_url = "http://localhost:8501"
    
    try:
        # Check Dashboard
        driver.get(base_url)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "stSidebar")))
        
        # Check Project Management
        project_link = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(text(), 'Projects')]")))
        project_link.click()
        
        print("UI Verification Started Successfully")
        
    except Exception as e:
        print(f"UI Verification Failed: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    verify_ui_components() 