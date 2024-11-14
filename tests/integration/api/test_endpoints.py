from fastapi.testclient import TestClient
from app.main import app

class TestAPIEndpoints:
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_hello_endpoint(self):
        response = self.client.get("/hello")
        assert response.status_code == 200
    
    def test_post_endpoint(self):
        response = self.client.post("/post", json={"key": "value"})
        assert response.status_code == 200
    
    # Additional endpoint tests... 