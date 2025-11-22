from app.database import engine
from sqlalchemy import text

def add_seller_id_column():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE orders ADD COLUMN seller_id INTEGER REFERENCES users(id) ON DELETE SET NULL"))
            conn.commit()
            print("Column 'seller_id' added successfully.")
        except Exception as e:
            print(f"Error adding 'seller_id' (maybe it exists): {e}")
            conn.rollback()

if __name__ == "__main__":
    add_seller_id_column()
