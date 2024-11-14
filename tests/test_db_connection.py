import os
import sys
import pytest
from sqlalchemy import text

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import engine, get_db
from app.models.project import Project
from app.models.competitor import Competitor
from app.models.service_area import ServiceArea
from app.db.base import Base

def test_database_connection():
    """Test basic database connectivity"""
    try:
        # Try to create a connection and execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.scalar() == 1
            print("Database connection successful!")
    except Exception as e:
        pytest.fail(f"Database connection failed: {str(e)}") 