import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def test_login(client):
    response = client.post('/api/login', json={'username': 'admin', 'password': 'admin'})
    assert response.status_code == 200
    assert 'access_token' in response.json


def test_add_ta_authorized(client):
    # login to get access token
    login_response = client.post('/api/login', json={'username': 'admin', 'password': 'admin'})
    assert login_response.status_code == 200
    access_token = login_response.json['access_token']

    # add TA with access token
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.post('/api/ta', headers=headers, json={
        'id': 2,
        'native_english_speaker': 2,
        'course_instructor': '15',
        'course': '3',
        'semester': 1,
        'class_size': 17,
        'performance_score': '3'})
    assert response.status_code == 201
    assert response.json['message'] == 'added successfully'


def test_get_ta_authorized(client):
    # login to get access token
    login_response = client.post('/api/login', json={'username': 'admin', 'password': 'admin'})
    assert login_response.status_code == 200
    access_token = login_response.json['access_token']

    # get TA with access token
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.get('/api/ta/1', headers=headers)
    assert response.status_code == 200
    assert response.json['id'] == 1


def test_update_ta_authorized(client):
    # login to get access token
    login_response = client.post('/api/login', json={'username': 'admin', 'password': 'admin'})
    assert login_response.status_code == 200
    access_token = login_response.json['access_token']

    # update TA with access token
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.put('/api/ta/1', headers=headers, json={
        'native_english_speaker': 4,
        'course_instructor': '15',
        'course': '5',
        'semester': 2,
        'class_size': 65,
        'performance_score': '3'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'TA updated successfully'


def test_delete_ta_authorized(client):
    # login to get access token
    login_response = client.post('/api/login', json={'username': 'admin', 'password': 'admin'})
    assert login_response.status_code == 200
    access_token = login_response.json['access_token']

    # delete TA with access token
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.delete('/api/ta/1', headers=headers)
    assert response.status_code == 200
    assert response.json['message'] == 'TA deleted successfully'
