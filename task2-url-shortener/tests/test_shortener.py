import pytest
import json
import tempfile
import os
from app.main import create_app
from models.database import init_db

@pytest.fixture
def client():
    """Create test client"""
    # Create temporary database
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app()
    app.config['TESTING'] = True
    app.config['DATABASE'] = db_path
    
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client
    
    os.close(db_fd)
    os.unlink(db_path)

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True

def test_shorten_url(client):
    """Test URL shortening"""
    url_data = {'url': 'https://www.example.com/very/long/url'}
    
    response = client.post('/api/shorten',
                          data=json.dumps(url_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'short_code' in data['data']
    assert len(data['data']['short_code']) == 6

def test_invalid_url(client):
    """Test shortening invalid URL"""
    url_data = {'url': 'not-a-valid-url'}
    
    response = client.post('/api/shorten',
                          data=json.dumps(url_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False

def test_redirect(client):
    """Test URL redirection"""
    # First shorten a URL
    url_data = {'url': 'https://www.example.com'}
    response = client.post('/api/shorten',
                          data=json.dumps(url_data),
                          content_type='application/json')
    
    data = json.loads(response.data)
    short_code = data['data']['short_code']
    
    # Then test redirect
    response = client.get(f'/{short_code}')
    assert response.status_code == 302
    assert response.location == 'https://www.example.com'

def test_stats(client):
    """Test getting URL statistics"""
    # First shorten a URL
    url_data = {'url': 'https://www.example.com'}
    response = client.post('/api/shorten',
                          data=json.dumps(url_data),
                          content_type='application/json')
    
    data = json.loads(response.data)
    short_code = data['data']['short_code']
    
    # Get stats
    response = client.get(f'/api/stats/{short_code}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data']['url'] == 'https://www.example.com'
    assert data['data']['clicks'] == 0

def test_click_tracking(client):
    """Test click count tracking"""
    # Shorten URL
    url_data = {'url': 'https://www.example.com'}
    response = client.post('/api/shorten',
                          data=json.dumps(url_data),
                          content_type='application/json')
    
    data = json.loads(response.data)
    short_code = data['data']['short_code']
    
    # Click the link
    client.get(f'/{short_code}')
    
    # Check stats
    response = client.get(f'/api/stats/{short_code}')
    data = json.loads(response.data)
    assert data['data']['clicks'] == 1

def test_nonexistent_short_code(client):
    """Test accessing nonexistent short code"""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    
    response = client.get('/api/stats/nonexistent')
    assert response.status_code == 404
