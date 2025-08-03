# Original database initialization
import sqlite3

def init_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    
    # Insert some test data
    cursor.execute("INSERT OR IGNORE INTO users (name, email, password) VALUES ('John Doe', 'john@example.com', '5d41402abc4b2a76b9719d911017c592')")
    cursor.execute("INSERT OR IGNORE INTO users (name, email, password) VALUES ('Jane Smith', 'jane@example.com', '5d41402abc4b2a76b9719d911017c592')")
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()
