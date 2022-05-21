import os
import sys

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "../"))

from typing import Optional, List
import json
from api_server.config import app, celery_app
from project.users.tasks import divide, get_page
from celery.result import AsyncResult

# uvicorn main:app  --reload --host 0.0.0.0 --port 8000


@app.get("/hello_world")
async def hello_world():
    return {"msg": "Hello World"}


@app.get("/new_task")
async def new_task():
    res = divide.delay(1, 2)
    return {"task_id": res.task_id}


@app.get("/task/{task_id}")
async def read_task(task_id):
    res = AsyncResult(task_id)
    if res.ready():
        if res.status == 'SUCCESS':
            return {'status': res.status, 'result': res.get()}
    return {'status': res.status}
