import json
from fastapi.testclient import TestClient
from text_processor_api_server.config import create_app
from jp_tokenizer.utils import parse_srt_file

app = create_app()

client = TestClient(app)


def test_read_index_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_read_jp_hello():
    response = client.get("/jp/hello_world")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_post_jp_text_payload_01():
    payload = {
        'content': ['test line 1']
    }
    response = client.post('/jp/convert', json=payload)
    assert response.status_code == 200
    assert response.json()['msg'] == 'ok'
    payload = response.json()['payload']
    print(payload['content'][0])
    assert len(payload['content'][0]) == 3


def test_post_jp_text_payload_02():
    payload = {
        'content': parse_srt_file()
    }
    response = client.post('/jp/convert', json=payload)
    assert response.status_code == 200
    assert response.json()['msg'] == 'ok'
    payload = response.json()['payload']
    assert len(payload['content']) == 1175

