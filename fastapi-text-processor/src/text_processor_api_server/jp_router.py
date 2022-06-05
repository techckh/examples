import os
import sys
import json
from typing import Any, Dict, AnyStr, List, Union
from jp_tokenizer.utils import convert_jp_text

from fastapi import APIRouter, Body
from pydantic import BaseModel

router = APIRouter()

JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]


class RequestData(BaseModel):
    content: List[Any]
    #content: str


@router.get("/hello_world")
async def hello_world():
    return {"msg": "Hello World"}


@router.post("/convert")
#async def convert_text(payload: JSONStructure = None):
async def convert_text(data: RequestData):
    lines = data.content
    output = convert_jp_text(lines)
    return {'msg': 'ok', 'payload': output}

