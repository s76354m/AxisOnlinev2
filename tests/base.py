import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

class BaseTest:
    @pytest.fixture(autouse=True)
    def setup(self, test_client: TestClient, db_session: Session):
        self.client = test_client
        self.db = db_session
        self.setup_test_data()
        
    def setup_test_data(self):
        """Override this method to set up test data"""
        pass 