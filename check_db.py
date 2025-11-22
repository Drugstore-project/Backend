import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "drugstore")
DB_USER = os.getenv("DB_USER", "druguser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "drugpass")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

print(f"Connecting to {DB_HOST}:{DB_PORT} as {DB_USER}...")

try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    print("SUCCESS: Connection established!")
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM products;")
    rows = cur.fetchall()
    print(f"Found {len(rows)} products:")
    for row in rows:
        print(row)
        
    conn.close()
except Exception as e:
    print(f"FAILURE: {e}")
