
from sqlalchemy import create_engine, inspect
from app.core.config import settings

# Use the database URL from settings or hardcode if necessary for the script
# Assuming settings.DATABASE_URL is available
try:
    from app.database import engine
except ImportError:
    # Fallback if app.database not easily importable in script context
    import os
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/drugstore_db")
    engine = create_engine(DATABASE_URL)

inspector = inspect(engine)
columns = inspector.get_columns('order_items')
batch_id_exists = any(c['name'] == 'batch_id' for c in columns)

print(f"batch_id column exists in order_items: {batch_id_exists}")
