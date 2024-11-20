import streamlit as st
import time
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Dict

class UITestRunner:
    def __init__(self):
        self.results: List[Tuple[str, str, str]] = []
        self.start_time = datetime.now()
        self.test_suites = {
            'Dashboard': self.run_dashboard_tests,
            'Service Area': self.run_service_area_tests,
            'Y-Line Management': self.run_yline_tests,
            'Project Management': self.run_project_tests,
            'CSP LOB Management': self.run_csp_lob_tests,
            'Competitor Management': self.run_competitor_tests,
            'Notes System': self.run_notes_tests
        }
    
    def run_all_tests(self):
        st.title("Comprehensive UI Test Suite")
        
        if st.button("Run All Tests"):
            with st.spinner("Running comprehensive test suite..."):
                for suite_name, test_func in self.test_suites.items():
                    self.run_test_suite(suite_name, test_func)
                
                self.display_results()
                self.generate_report()
    
    def run_test_suite(self, suite_name: str, test_func: callable):
        try:
            with st.expander(f"Running {suite_name}"):
                results = test_func()
                self.results.extend(results)
        except Exception as e:
            self.results.append((suite_name, "ERROR", str(e)))
    
    def display_results(self):
        st.header("Test Results")
        df = pd.DataFrame(self.results, columns=["Component", "Status", "Details"])
        st.dataframe(df)
        
        # Summary statistics
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r[1] == "Success")
        st.metric("Test Coverage", f"{passed_tests}/{total_tests}") 