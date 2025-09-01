import pytest
from app import create_app, db
from app.models.user import User

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_user(client):
    """Test user registration"""
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'password123',
        'first_name': 'Test',
        'last_name': 'User'
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert 'access_token' in data
    assert data['user']['email'] == 'test@example.com'

def test_login_user(client):
    """Test user login"""
    # First register a user
    client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'password123'
    })
    
    # Then login
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data

def test_invalid_login(client):
    """Test invalid login credentials"""
    response = client.post('/api/auth/login', json={
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 401
