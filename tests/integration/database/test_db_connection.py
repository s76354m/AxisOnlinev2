import pytest
from sqlalchemy import text
from app.db.session import get_db, engine

def test_database_connection():
    """Test that we can connect to the database"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.scalar() == 1
    except Exception as e:
        pytest.fail(f"Database connection failed: {str(e)}")

def test_get_db():
    """Test that get_db yields a working session"""
    db = next(get_db())
    try:
        result = db.execute(text("SELECT 1"))
        assert result.scalar() == 1
    finally:
        db.close()

def test_database_tables():
    """Test that all required tables exist"""
    from app.db.base import Base
    
    # Get all table names from our models
    expected_tables = {table.lower() for table in Base.metadata.tables.keys()}
    
    # Get actual tables from database
    with engine.connect() as connection:
        result = connection.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_type = 'BASE TABLE'
        """))
        actual_tables = {row[0].lower() for row in result}
    
    # Check that all our models have corresponding tables
    missing_tables = expected_tables - actual_tables
    assert not missing_tables, f"Missing tables: {missing_tables}" 