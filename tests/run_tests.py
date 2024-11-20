import streamlit as st
import time
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_all_tests():
    st.title("Test Suite Dashboard")
    
    if st.button("Run All Tests"):
        with st.spinner("Running tests..."):
            results = []
            
            # Functional Tests
            results.extend(test_project_management())
            results.extend(test_service_area())
            results.extend(test_competitor_management())
            results.extend(test_notes_system())
            results.extend(test_y_line_management())
            
            # UI Tests
            results.extend(run_dashboard_tests())
            results.extend(run_navigation_tests())
            results.extend(run_performance_tests())
            
            # Display results
            st.table({
                "Feature": [r[0] for r in results],
                "Status": [r[1] for r in results],
                "Details": [r[2] for r in results]
            })
            
            # Generate report
            generate_test_report(results)

def generate_test_report(results):
    """Generate detailed test report"""
    report_path = Path("test_reports") / f"test_report_{datetime.now():%Y%m%d_%H%M}.html"
    report_path.parent.mkdir(exist_ok=True)
    
    with report_path.open('w') as f:
        f.write(generate_html_report(results))

if __name__ == "__main__":
    run_all_tests() 