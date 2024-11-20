import streamlit as st
from datetime import datetime
from pathlib import Path

def run_all_ui_tests():
    st.title("UI Test Suite")
    
    # Configure test environment
    setup_test_environment()
    
    # Run test categories
    results = []
    results.extend(run_dashboard_tests())
    results.extend(run_navigation_tests())
    results.extend(run_performance_tests())
    
    # Generate report
    generate_test_report(results)
    
    # Display results
    display_test_results(results)

def generate_test_report(results):
    """Generate detailed test report"""
    report_path = Path("test_reports") / f"ui_test_report_{datetime.now():%Y%m%d_%H%M}.html"
    report_path.parent.mkdir(exist_ok=True)
    
    with report_path.open('w') as f:
        f.write(generate_html_report(results)) 