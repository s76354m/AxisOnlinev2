"""Test runner script"""
import pytest
import os
from datetime import datetime

def run_tests():
    """Execute test suite"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = "test_reports"
    
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    pytest_args = [
        "-v",
        f"--html={report_dir}/report_{timestamp}.html",
        "--self-contained-html",
        "tests/"
    ]
    
    return pytest.main(pytest_args)

if __name__ == "__main__":
    exit_code = run_tests()
    print(f"Test suite completed with exit code: {exit_code}") 