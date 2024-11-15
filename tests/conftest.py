"""Test configuration and fixtures"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.core.config import settings
from app.models.project import Project
from app.models.csp_lob import CSPLOB
from app.models.y_line import YLine

@pytest.fixture(scope="session")
def driver():
    """Setup WebDriver for tests"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def base_url():
    """Base URL for Streamlit application"""
    return "http://localhost:8501"

@pytest.fixture(scope="session")
def engine():
    return create_engine(settings.TEST_DATABASE_URL)

@pytest.fixture(scope="session")
def TestingSessionLocal(engine):
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal

@pytest.fixture
def db_session(TestingSessionLocal):
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture
def test_project(db_session):
    """Create a test project"""
    project = Project(
        ProjectType="Translation",
        ProjectDesc="Test Project",
        Status="New",
        Analyst="Test Analyst",
        PM="Test PM",
        LastEditMSID="TEST"
    )
    db_session.add(project)
    db_session.commit()
    return project

@pytest.fixture
def test_csp_lob(db_session):
    """Create a test CSP LOB mapping"""
    csp_lob = CSPLOB(
        csp_code="TEST123",
        lob_type="Medical",
        description="Test LOB",
        status="Active",
        created_by="TEST"
    )
    db_session.add(csp_lob)
    db_session.commit()
    return csp_lob