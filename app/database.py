from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base

# Base is imported to be available for other modules

SQLALCHEMY_DATABASE_URL = settings.database_url

print(f"DATABASE CONFIG: Connecting to {SQLALCHEMY_DATABASE_URL.split('@')[-1] if '@' in SQLALCHEMY_DATABASE_URL else 'SQLite/Local'}")

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency FastAPI: abre/fecha sessão por request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
