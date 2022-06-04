import os
import sys
from jp_tokenizer.utils import get_compound_verbs_tables


#BASE_DIR = os.path.dirname(os.path.realpath(__file__))
#sys.path.insert(0, os.path.join(BASE_DIR, "../"))

import json
from typing import Any, Dict, AnyStr, List, Union
from fastapi import Depends, FastAPI, HTTPException
from .config import create_app


# uvicorn main:app  --reload --host 0.0.0.0 --port 8000
