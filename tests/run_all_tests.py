import streamlit as st
import pytest
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

class TestRunner:
    def __init__(self):
        self.results: Dict[str, List[Dict[str, Any]]] = {
            'ui': [],
            'integration': [],
            'e2e': [],
            'performance': []
        }
        
    def run_all_tests(self):
        st.title("Comprehensive Test Suite")
        
        if st.button("Run All Tests"):
            with st.spinner("Running tests..."):
                # Run UI tests
                self._run_test_category('ui', [
                    'tests/ui/dashboard',
                    'tests/ui/project_management',
                    'tests/ui/competitor_management'
                ])
                
                # Run integration tests
                self._run_test_category('integration', [
                    'tests/integration/ui',
                    'tests/integration/api'
                ])
                
                # Run E2E tests
                self._run_test_category('e2e', [
                    'tests/e2e/ui',
                    'tests/e2e/workflows'
                ])
                
                # Run performance tests
                self._run_test_category('performance', [
                    'tests/performance'
                ])
                
                self._display_results()
                self._generate_report()
    
    def _run_test_category(self, category: str, paths: List[str]):
        for path in paths:
            result = pytest.main([path, '-v'])
            self.results[category].append({
                'path': path,
                'status': 'Success' if result == 0 else 'Failed',
                'timestamp': datetime.now().isoformat()
            })
    
    def _display_results(self):
        st.header("Test Results")
        for category, results in self.results.items():
            st.subheader(category.upper())
            st.table(results)
    
    def _generate_report(self):
        report_path = Path("test_reports") / f"test_report_{datetime.now():%Y%m%d_%H%M}.html"
        # Generate HTML report implementation 