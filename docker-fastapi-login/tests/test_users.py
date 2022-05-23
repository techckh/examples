from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_login import create_app

app = create_app()

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_get_user():
    exp_data = {
        'id': 1,
        'email': 'admin@test.com'
    }
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == exp_data


def test_get_users():
    exp_data = {
        'id': 1,
        'email': 'admin@test.com'
    }
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    data = data[0]
    assert data == exp_data


def test_get_token_invalid_user():
    form_data = {
        'username': 'non_existing_user@test.com',
        'password': '123456',
    }
    response = client.post("/users/token", data=form_data)
    assert response.status_code == 401


def test_get_token():
    form_data = {
        'username': 'admin@test.com',
        'password': '123456',
    }
    response = client.post("/users/token", data=form_data)
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'

    headers = dict()
    headers['Authorization'] = 'bearer {}'.format(data['access_token'])
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'password' not in data
    assert data['email'] == 'admin@test.com'
