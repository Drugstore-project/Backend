import sqlite3
import os

def check_sqlite_users():
    db_path = "drugstore.db"
    if not os.path.exists(db_path):
        print(f"SQLite database '{db_path}' not found.")
        return

    print(f"Checking SQLite database: {db_path}")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        if not cursor.fetchone():
            print("Table 'users' does not exist in SQLite.")
            return

        cursor.execute("SELECT id, email, password_hash FROM users;")
        users = cursor.fetchall()
        
        print(f"Found {len(users)} users in SQLite:")
        for user in users:
            print(f" - ID: {user[0]}, Email: {user[1]}, Hash: {user[2]}")
            
        conn.close()
    except Exception as e:
        print(f"Error reading SQLite: {e}")

if __name__ == "__main__":
    check_sqlite_users()
