import os
from datetime import datetime, timedelta

from typing import List, Union
from sqlalchemy.orm import Session

from pydantic import BaseModel
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from fastapi_login.users import schemas
from .crud import get_user, get_users, get_user_by_email
from fastapi_login.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    secret_key = os.getenv('SECRET_KEY')
    algorithm = os.getenv('ALGORITHM')
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


@router.get("/me", response_model=schemas.User)
async def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    db_user = get_current_user(db, token)
    if db_user and db_user.is_active:
        return schemas.UserInDB(**jsonable_encoder(db_user))
    raise HTTPException(status_code=400, detail="Inactive user")


@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    return user


@router.get("/", response_model=List[schemas.User])
async def read_users(db: Session = Depends(get_db)):
    users = get_users(db)
    return users


def get_current_user(db: Session, token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        secret_key = os.getenv('SECRET_KEY')
        algorithm = os.getenv('ALGORITHM')
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    db_user = get_user_by_email(db, token_data.username)
    if db_user is None:
        raise credentials_exception
    return db_user


def authenticate_user(db, email: str, password: str):
    db_user = get_user_by_email(db, email)
    if not db_user:
        return False
    if not verify_password(password, db_user.password):
        return False
    return schemas.UserInDB(**jsonable_encoder(db_user))


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    expire_mins = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    access_token_expires = timedelta(minutes=expire_mins)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
