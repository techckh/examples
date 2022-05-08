import time
from fastapi.testclient import TestClient
from api_server.main import app

client = TestClient(app)


def test_app_hello_world():
    res = client.get("/hello_world")
    assert res.status_code == 200
    assert res.json() == {"msg": "Hello World"}


def test_app_new_task():
    res = client.get("/new_task")
    assert res.status_code == 200
    data = res.json()
    assert 'task_id' in data
    task_id = data['task_id']
    time.sleep(3.5)
    res = client.get('/task/{}'.format(task_id))
    assert res.status_code == 200
    data = res.json()
    assert data['status'] == 'SUCCESS'
    print(data['result'])
