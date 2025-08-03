import pytest
import tempfile
import os
from models.user import User
from models.database import init_db
from config import Config

@pytest.fixture
def setup_test_db():
    """Setup test database"""
    # Create temporary database file
    db_fd, Config.DATABASE_URL = tempfile.mkstemp()
    Config.DATABASE_URL = f"sqlite:///{Config.DATABASE_URL}"
    
    init_db()
    
    yield
    
    # Cleanup
    os.close(db_fd)
    os.unlink(Config.DATABASE_URL.replace('sqlite:///', ''))

def test_create_user(setup_test_db):
    """Test user creation"""
    user = User.create("John Doe", "john@example.com", "password123")
    
    assert user.id is not None
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
    assert user.password_hash is not None

def test_get_user_by_id(setup_test_db):
    """Test getting user by ID"""
    user = User.create("Jane Doe", "jane@example.com", "password123")
    retrieved_user = User.get_by_id(user.id)
    
    assert retrieved_user is not None
    assert retrieved_user.name == "Jane Doe"
    assert retrieved_user.email == "jane@example.com"

def test_password_hashing(setup_test_db):
    """Test password hashing and verification"""
    user = User.create("Test User", "test@example.com", "password123")
    
    assert user.check_password("password123") is True
    assert user.check_password("wrongpassword") is False
