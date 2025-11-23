import os
from app.core.config import settings

def check_db_config():
    print(f"ENV: {os.getenv('ENV')}")
    print(f"DATABASE_URL env var: {os.getenv('DATABASE_URL')}")
    print(f"Settings database_url: {settings.database_url}")
    
    if "sqlite" in settings.database_url:
        print("WARNING: Using SQLite. Data will be lost on restart/deploy.")
    else:
        print("Using PostgreSQL (or other external DB).")

if __name__ == "__main__":
    check_db_config()
