import sqlite3
import threading
from contextlib import contextmanager

# Thread-local storage for database connections
_local = threading.local()

def get_db_connection():
    """Get database connection with thread safety"""
    if not hasattr(_local, 'connection'):
        _local.connection = sqlite3.connect('url_shortener.db', check_same_thread=False)
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
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                clicks INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_short_code ON urls(short_code)')
