"""Performance tests"""
import pytest
import time
from locust import HttpUser, task, between
from app.core.config import settings

class ProjectLoadTest(HttpUser):
    wait_time = between(1, 2)
    
    @task
    def test_project_list(self):
        """Test project list performance"""
        start_time = time.time()
        response = self.client.get("/api/v1/projects/")
        end_time = time.time()
        
        assert response.status_code == 200
        assert end_time - start_time < 1.0  # Response under 1 second
    
    @task
    def test_project_creation(self):
        """Test project creation performance"""
        start_time = time.time()
        response = self.client.post(
            "/api/v1/projects/",
            json={
                "ProjectType": "Translation",
                "ProjectDesc": "Performance Test",
                "Status": "New",
                "Analyst": "Test",
                "PM": "Test"
            }
        )
        end_time = time.time()
        
        assert response.status_code == 201
        assert end_time - start_time < 2.0  # Creation under 2 seconds 