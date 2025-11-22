from app.database import engine
from sqlalchemy import text

def add_column():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE products ADD COLUMN min_stock_level INTEGER DEFAULT 10"))
            conn.commit()
            print("Column min_stock_level added successfully.")
        except Exception as e:
            print(f"Error (maybe column exists): {e}")

if __name__ == "__main__":
    add_column()
