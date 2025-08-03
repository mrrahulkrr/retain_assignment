from typing import Optional, List, Dict, Any
from models.database import get_db
import bcrypt
from utils.validators import validate_email, validate_password

class User:
    """User model with proper encapsulation"""
    
    def __init__(self, id: int = None, name: str = None, email: str = None, 
                 password_hash: str = None, created_at: str = None, updated_at: str = None):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
        self.updated_at = updated_at
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """Check if provided password matches hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert user to dictionary (excluding sensitive data by default)"""
        user_dict = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        
        if include_sensitive:
            user_dict['password_hash'] = self.password_hash
            
        return user_dict
    
    @classmethod
    def create(cls, name: str, email: str, password: str) -> 'User':
        """Create a new user with validation"""
        # Validate input
        if not validate_email(email):
            raise ValueError("Invalid email format")
        
        if not validate_password(password):
            raise ValueError("Password must be at least 8 characters long")
        
        if not name or len(name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters long")
        
        # Hash password
        password_hash = cls.hash_password(password)
        
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                    (name.strip(), email.lower().strip(), password_hash)
                )
                user_id = cursor.lastrowid
                return cls.get_by_id(user_id)
            except sqlite3.IntegrityError:
                raise ValueError("Email already exists")
    
    @classmethod
    def get_by_id(cls, user_id: int) -> Optional['User']:
        """Get user by ID"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            
            if row:
                return cls(**dict(row))
            return None
    
    @classmethod
    def get_by_email(cls, email: str) -> Optional['User']:
        """Get user by email"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email.lower().strip(),))
            row = cursor.fetchone()
            
            if row:
                return cls(**dict(row))
            return None
    
    @classmethod
    def get_all(cls, limit: int = 100, offset: int = 0) -> List['User']:
        """Get all users with pagination"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?", (limit, offset))
            rows = cursor.fetchall()
            
            return [cls(**dict(row)) for row in rows]
    
    @classmethod
    def search_by_name(cls, name: str, limit: int = 50) -> List['User']:
        """Search users by name"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE name LIKE ? ORDER BY name LIMIT ?",
                (f"%{name.strip()}%", limit)
            )
            rows = cursor.fetchall()
            
            return [cls(**dict(row)) for row in rows]
    
    def update(self, name: str = None, email: str = None) -> bool:
        """Update user information"""
        if not self.id:
            raise ValueError("Cannot update user without ID")
        
        updates = {}
        if name is not None:
            if len(name.strip()) < 2:
                raise ValueError("Name must be at least 2 characters long")
            updates['name'] = name.strip()
        
        if email is not None:
            if not validate_email(email):
                raise ValueError("Invalid email format")
            updates['email'] = email.lower().strip()
        
        if not updates:
            return False
        
        # Build dynamic query
        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values()) + [self.id]
        
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    f"UPDATE users SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    values
                )
                
                # Update instance attributes
                for key, value in updates.items():
                    setattr(self, key, value)
                
                return cursor.rowcount > 0
            except sqlite3.IntegrityError:
                raise ValueError("Email already exists")
    
    def delete(self) -> bool:
        """Delete user"""
        if not self.id:
            raise ValueError("Cannot delete user without ID")
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (self.id,))
            return cursor.rowcount > 0
