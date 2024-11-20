"""Test configuration and fixtures"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class MockModel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @classmethod
    def query(cls):
        return MockQuery()

class MockQuery:
    def filter_by(self, **kwargs):
        return self
    
    def first(self):
        return MockModel()
    
    def all(self):
        return []

class MockService:
    def __getattr__(self, name):
        return Mock(return_value=True)

@pytest.fixture(autouse=True)
def mock_dependencies(monkeypatch):
    # Mock services
    monkeypatch.setattr('app.services.security.SecurityService', MockService)
    monkeypatch.setattr('app.services.auth.AuthService', MockService)
    monkeypatch.setattr('app.services.csp_lob.CSPLOBService', MockService)
    
    # Mock models
    monkeypatch.setattr('app.models.CSPLOB', MockModel)
    monkeypatch.setattr('app.models.Project', MockModel)
    monkeypatch.setattr('app.models.YLine', MockModel)
    monkeypatch.setattr('app.models.Competitor', MockModel)

@pytest.fixture
def selenium_driver():
    driver = Mock()
    driver.implicitly_wait = Mock()
    driver.maximize_window = Mock()
    driver.get = Mock()
    driver.find_element = Mock(return_value=Mock())
    driver.find_elements = Mock(return_value=[Mock()])
    return driver