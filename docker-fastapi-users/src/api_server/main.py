import os
import sys

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "../"))

from typing import Optional, List
import json
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi_login import create_app
from fastapi_login.database import SessionLocal, engine

# uvicorn main:app  --reload --host 0.0.0.0 --port 8000
app = create_app()


@app.get("/hello_world")
async def hello_world():
    return {"msg": "Hello World"}


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
"""

"""
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
"""
