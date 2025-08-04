from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import uuid4

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str

class Post(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    body: str = Field(default=None)
    date: Optional[str] = Field(default=None)