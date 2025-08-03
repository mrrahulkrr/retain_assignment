import sqlite3
import threading
from contextlib import contextmanager
from config import Config

# Thread-local storage for database connections
_local = threading.local()

def get_db_connection():
    """Get database connection with thread safety"""
    if not hasattr(_local, 'connection'):
        _local.connection = sqlite3.connect(
            Config.DATABASE_URL.replace('sqlite:///', ''),
            check_same_thread=False
        )
        _local.connection.row_factory = sqlite3.Row
    return _local.connection

@contextmanager
def get_db():
    """Context manager for database operations"""
    conn = get_db_connection()
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()

def init_db():
    """Initialize database with proper schema"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Created indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_name ON users(name)')
