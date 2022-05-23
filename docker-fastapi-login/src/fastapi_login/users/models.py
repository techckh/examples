from sqlalchemy import Column, Integer, String, Boolean

from fastapi_login.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(200), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean)
    # name = Column(String(200), unique=True, nullable=True)

    def __init__(self, email, password, *args, **kwargs):
        self.email = email
        self.password = password
