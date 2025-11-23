import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "drugstore")
DB_USER = os.getenv("DB_USER", "druguser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "drugpass")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    
    # Find users that look like test users (Pharmacist XXXX)
    print("Searching for test users...")
    cur.execute("SELECT id, name, email, role_id FROM users WHERE name LIKE 'Pharmacist %' OR email LIKE 'pharm%@drugstore.com';")
    rows = cur.fetchall()
    
    if not rows:
        print("No test users found.")
    else:
        print(f"Found {len(rows)} test users:")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Role ID: {row[3]}")
            
            # Delete them
            print(f"Deleting user {row[1]}...")
            cur.execute("DELETE FROM users WHERE id = %s;", (row[0],))
            conn.commit()
            print("Deleted.")

    conn.close()
    print("Cleanup complete.")

except Exception as e:
    print(f"Error: {e}")
