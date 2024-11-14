import pytest
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

def test_db_connection():
    """Test basic database connectivity"""
    # Load environment variables
    load_dotenv()
    
    # Get connection details
    server = os.getenv("DB_SERVER", "DESKTOP-PJTAP42\\SQLEXPRESS")
    database = os.getenv("DB_NAME", "ndar")
    driver = os.getenv("DB_DRIVER", "ODBC+Driver+17+for+SQL+Server")
    
    # Create connection string
    connection_string = f"mssql+pyodbc://{server}/{database}?driver={driver}&trusted_connection=yes"
    
    try:
        # Create engine and test connection
        engine = create_engine(connection_string)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.scalar() == 1
            print("Database connection successful!")
    except Exception as e:
        pytest.fail(f"Database connection failed: {str(e)}")

if __name__ == "__main__":
    test_db_connection() 