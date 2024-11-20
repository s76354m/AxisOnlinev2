import click
import pytest
import os
from pathlib import Path
from datetime import datetime
import json

@click.group()
def cli():
    """UI Testing Command Line Interface"""
    pass

@cli.command()
@click.option('--suite', default='all', help='Test suite to run (ui/e2e/integration/all)')
@click.option('--browser', default='chrome', help='Browser for UI tests')
@click.option('--report/--no-report', default=True, help='Generate test report')
def test(suite, browser, report):
    """Run test suites"""
    os.environ['PYTEST_ADDOPTS'] = f'--driver {browser}'
    
    # Reference test paths from run_comprehensive_tests.py
    test_paths = {
        'Dashboard': ['tests/ui/dashboard', 'tests/e2e/dashboard'],
        'Security': ['tests/security'],
        'Project Management': ['tests/ui/project_management'],
        'Service Area': ['tests/ui/service_area'],
        'CSP LOB': ['tests/ui/csp_lob'],
        'Competitor': ['tests/ui/competitor'],
        'Notes': ['tests/ui/notes']
    }
    
    if suite == 'all':
        paths = [path for paths in test_paths.values() for path in paths]
    else:
        paths = test_paths.get(suite, [])
    
    # Create directories if needed
    for path in paths:
        os.makedirs(path, exist_ok=True)
    
    # Run tests and generate report
    results = pytest.main(['--verbose'] + paths)
    
    if report:
        generate_report(results, suite, browser)

def generate_report(results, suite, browser):
    """Generate test report"""
    report = {
        'suite': suite,
        'browser': browser,
        'timestamp': datetime.now().isoformat(),
        'results': results
    }
    
    report_path = Path('test_reports')
    report_path.mkdir(exist_ok=True)
    
    with open(report_path / f'report_{suite}_{datetime.now():%Y%m%d_%H%M%S}.json', 'w') as f:
        json.dump(report, f, indent=2)

if __name__ == '__main__':
    cli() 