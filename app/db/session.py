from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import Settings
from app.utils.db_monitor import DatabaseMonitor

settings = Settings()
db_monitor = DatabaseMonitor()

# Create engine using the settings
try:
    engine = create_engine(settings.DATABASE_URL, echo=settings.DB_ECHO)
    
    @event.listens_for(engine, 'connect')
    def receive_connect(dbapi_connection, connection_record):
        db_monitor.log_operation('connection', 'success')
    
    @event.listens_for(engine, 'disconnect')
    def receive_disconnect(dbapi_connection, connection_record):
        db_monitor.log_operation('disconnection', 'success')

except SQLAlchemyError as e:
    db_monitor.log_error('engine_creation', e)
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db_monitor.log_error('session_creation', e)
        raise
    finally:
        db.close()