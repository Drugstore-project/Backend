"""
Database connection and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base

# pylint: disable=unused-import
# Base is imported to be available for other modules

SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency FastAPI: abre/fecha sessão por request
def get_db():
    """
    Creates a new database session for a request and closes it afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
