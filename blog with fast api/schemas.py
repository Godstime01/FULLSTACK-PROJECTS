from pydantic import BaseModel
from typing import Optional
import datetime


class User(BaseModel):

    username: str
    email:str
    password: str

class UserOutput(BaseModel):
    id: int
    username: str
    email:str

class Post(BaseModel):
    id: int
    title: str
    body: str
    is_published: bool
    author_id: int


class Comment(BaseModel):
    id: int
    post_id: int
    comment: str
    user_id: int

class Token(BaseModel):
    access_token: str
    token_type: str

class DataToken(BaseModel):
    id:Optional[str] = None