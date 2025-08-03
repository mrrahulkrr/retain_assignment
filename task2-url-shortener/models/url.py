from typing import Optional, Dict, Any
from models.database import get_db
from utils.validators import validate_url
from utils.code_generator import generate_short_code
import sqlite3
from datetime import datetime

class URL:
    """URL model for shortener service"""
    
    def __init__(self, id: int = None, short_code: str = None, original_url: str = None,
                 clicks: int = 0, created_at: str = None):
        self.id = id
        self.short_code = short_code
        self.original_url = original_url
        self.clicks = clicks
        self.created_at = created_at
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert URL to dictionary"""
        return {
            'id': self.id,
            'short_code': self.short_code,
            'original_url': self.original_url,
            'clicks': self.clicks,
            'created_at': self.created_at
        }
    
    @classmethod
    def create(cls, original_url: str) -> 'URL':
        """Create a new short URL"""
        # Validate URL
        if not validate_url(original_url):
            raise ValueError("Invalid URL format")
        
        # Generate unique short code
        max_attempts = 10
        for _ in range(max_attempts):
            short_code = generate_short_code()
            
            with get_db() as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO urls (short_code, original_url) VALUES (?, ?)",
                        (short_code, original_url)
                    )
                    url_id = cursor.lastrowid
                    return cls.get_by_id(url_id)
                except sqlite3.IntegrityError:
                    # Short code collision, try again
                    continue
        
        raise RuntimeError("Failed to generate unique short code after multiple attempts")
    
    @classmethod
    def get_by_id(cls, url_id: int) -> Optional['URL']:
        """Get URL by ID"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM urls WHERE id = ?", (url_id,))
            row = cursor.fetchone()
            
            if row:
                return cls(**dict(row))
            return None
    
    @classmethod
    def get_by_short_code(cls, short_code: str) -> Optional['URL']:
        """Get URL by short code"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM urls WHERE short_code = ?", (short_code,))
            row = cursor.fetchone()
            
            if row:
                return cls(**dict(row))
            return None
    
    def increment_clicks(self) -> bool:
        """Increment click count for this URL"""
        if not self.id:
            return False
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE urls SET clicks = clicks + 1 WHERE id = ?",
                (self.id,)
            )
            
            if cursor.rowcount > 0:
                self.clicks += 1
                return True
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics for this URL"""
        return {
            'url': self.original_url,
            'clicks': self.clicks,
            'created_at': self.created_at
        }
