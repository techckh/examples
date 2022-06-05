import os
from dotenv import load_dotenv
import requests
from jp_tokenizer.utils import parse_srt_file

load_dotenv()
server_url = 'http://localhost:8080'
#server_url = os.getenv('GCLOUD_ENDPOINT')
assert server_url


def test_app_index():
    response = requests.get(server_url)
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_jp_index():
    response = requests.get("{}/jp/hello_world".format(server_url))
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_jp_convert_payload_01():
    payload = {
        'content': ['test line 1']
    }
    response = requests.post('{}/jp/convert'.format(server_url), json=payload)
    assert response.status_code == 200
    assert response.json()['msg'] == 'ok'
    payload = response.json()['payload']
    print(payload['content'][0])
    assert len(payload['content'][0]) == 3


def test_jp_convert_payload_02():
    payload = {
        'content': parse_srt_file()
    }
    response = requests.post('{}/jp/convert'.format(server_url), json=payload)
    assert response.status_code == 200
    assert response.json()['msg'] == 'ok'
    payload = response.json()['payload']
    assert len(payload['content']) == 1175
