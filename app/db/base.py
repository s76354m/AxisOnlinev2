from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

def init_db(engine):
    # Import all models here to ensure they're registered
    from app.models import Project, Competitor, ServiceArea, YLine, ProjectNote
    Base.metadata.create_all(bind=engine) 