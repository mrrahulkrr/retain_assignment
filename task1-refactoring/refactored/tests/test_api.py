import pytest
import json
from app import create_app
from models.database import init_db
from config import Config
import tempfile
import os

@pytest.fixture
def client():
    """Create test client"""
    db_fd, Config.DATABASE_URL = tempfile.mkstemp()
    Config.DATABASE_URL = f"sqlite:///{Config.DATABASE_URL}"
    
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client
    
    os.close(db_fd)
    os.unlink(Config.DATABASE_URL.replace('sqlite:///', ''))

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_create_user(client):
    """Test user creation endpoint"""
    user_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': 'password123'
    }
    
    response = client.post('/api/users', 
                          data=json.dumps(user_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data']['name'] == 'John Doe'

def test_login(client):
    """Test login endpoint"""
    # First create a user
    user_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': 'password123'
    }
    client.post('/api/users', 
                data=json.dumps(user_data),
                content_type='application/json')
    
    # Then try to login
    login_data = {
        'email': 'john@example.com',
        'password': 'password123'
    }
    
    response = client.post('/api/login',
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
