import os
import sys

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "../"))

import json
from typing import Optional, List
from fastapi import Depends, FastAPI, HTTPException
from .config import create_app


# uvicorn main:app  --reload --host 0.0.0.0 --port 8000
app = create_app()


@app.get("/hello_world")
async def hello_world():
    return {"msg": "Hello World"}

