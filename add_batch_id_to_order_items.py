from app.database import engine
from sqlalchemy import text

def add_column():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE order_items ADD COLUMN batch_id INTEGER REFERENCES product_batches(id)"))
            conn.commit()
            print("Column batch_id added successfully.")
        except Exception as e:
            print(f"Error (maybe column exists): {e}")

if __name__ == "__main__":
    add_column()
