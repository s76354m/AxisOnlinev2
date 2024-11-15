from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging

# Set up logging
logger = logging.getLogger(__name__)

try:
    # Create engine using Windows Authentication
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DB_ECHO,
        pool_pre_ping=True
    )

    # Test the connection
    with engine.connect() as connection:
        logger.info("Successfully connected to database")

except Exception as e:
    logger.error(f"Error connecting to database: {str(e)}")
    raise

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database with required tables"""
    from app.db.base import Base  # Import all models here
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise 