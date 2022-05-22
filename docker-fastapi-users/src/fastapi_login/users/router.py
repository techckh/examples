from typing import List, Union
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer

from fastapi_login.users import schemas
#from fastapi_myproject.generated.user.crud_mongo import insert_user, find_user, update_user
from .crud import get_user, get_users
from fastapi_login.database import SessionLocal, engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def fake_decode_token(token):
    #return schemas.User(username=token + "fakedecoded", email="john@example.com", full_name="John Doe")
    return schemas.User(username=token + "fakedecoded", email="john@example.com", full_name="John Doe")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    #user = fake_decode_token(token)
    return schemas.User(id=1, email='test@test.com')


@router.get("/me")
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    return user


@router.get("/", response_model=List[schemas.User])
async def read_users(db: Session = Depends(get_db)):
    users = get_users(db)
    return users



"""
@router.post("/")
def create_user(item: schemas.User):
    result_id = insert_user(db, item)
    return {"item_id": result_id}


@router.get("/{item_id}", response_model=schemas.User)
def read_user(item_id: str):
    item = find_user(db, item_id)
    return item


@router.put("/{item_id}")
def update_user(item_id: str, item: schemas.User):
    count = update_user(db, item_id, item)
    return {"modified_count": count}


@router.delete("/{item_id}")
def delete_user(item_id: str):
    count = delete_user(db, item_id)
    return {"deleted_count": count}
"""


"""
@router.get("/")
async def read_items():
    return [{"name": "Item Foo"}, {"name": "item Bar"}]


@router.get("/{item_id}")
async def read_item(item_id: str):
    return {"name": "Fake Specific Item", "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "foo":
        raise HTTPException(status_code=403, detail="You can only update the item: foo")
    return {"item_id": item_id, "name": "The Fighters"}
"""