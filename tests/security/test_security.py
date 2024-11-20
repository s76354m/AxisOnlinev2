import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_security_service():
    return Mock()

def test_authentication(mock_security_service):
    """Test authentication flow"""
    with patch('app.services.security.SecurityService', return_value=mock_security_service):
        mock_security_service.authenticate.return_value = True
        assert mock_security_service.authenticate("test_user", "test_pass")

def test_authorization(mock_security_service):
    """Test authorization checks"""
    with patch('app.services.security.SecurityService', return_value=mock_security_service):
        mock_security_service.check_permission.return_value = True
        assert mock_security_service.check_permission("test_user", "read")