from app.database import engine
from sqlalchemy import text

def create_batch_table():
    with engine.connect() as conn:
        try:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS product_batches (
                    id SERIAL PRIMARY KEY,
                    product_id INTEGER NOT NULL REFERENCES products(id),
                    batch_number VARCHAR(50) NOT NULL,
                    quantity INTEGER NOT NULL,
                    expiration_date DATE NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                )
            """))
            conn.commit()
            print("Table 'product_batches' created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")
            conn.rollback()

if __name__ == "__main__":
    create_batch_table()
