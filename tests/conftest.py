import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

@pytest.fixture(scope="session")
def test_app():
    from app.main import app
    client = TestClient(app)
    yield client

@pytest.fixture(scope="session")
def db_session():
    from app.db.session import SessionLocal
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def test_client(test_app):
    return test_app