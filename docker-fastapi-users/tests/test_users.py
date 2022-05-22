from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_login import create_app

app = create_app()

"""
@app.get("/")
async def read_main():
    return {"msg": "Hello World"}
"""
client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_get_user_me():
    exp_data = {
        'id': 1,
        'email': 'admin@test.com'
    }
    headers = {'Authorization': 'bearer token'}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json() == exp_data


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
