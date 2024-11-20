from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from contextlib import contextmanager
from typing import Generator
import logging

logger = logging.getLogger(__name__)

def create_db_engine() -> Engine:
    connection_string = "mssql+pyodbc:///?odbc_connect=DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-PJTAP42\\SQLEXPRESS;DATABASE=ndar;Trusted_Connection=yes;"
    engine = create_engine(
        connection_string,
        pool_pre_ping=True,
        pool_recycle=3600
    )
    return engine

engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Engine event listeners
@event.listens_for(Engine, "connect")
def connect(dbapi_connection, connection_record):
    logger.info("Database connection established")

@event.listens_for(Engine, "engine_connect")
def ping_connection(connection, branch):
    if branch:
        return

    try:
        connection.scalar(text("SELECT 1"))
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise