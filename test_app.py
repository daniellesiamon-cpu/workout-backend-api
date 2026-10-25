import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_workouts(client):
    response = client.get('/workouts')
    assert response.status_code == 200

def test_get_exercises(client):
    response = client.get('/exercises')
    assert response.status_code == 200
