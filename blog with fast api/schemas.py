from pydantic import BaseModel, validator
import datetime


class User(BaseModel):
    username: str
    password: str


class Post(BaseModel):
    title: str
    body: str
    is_published: bool
    author_id: int


class Comment(BaseModel):
    post_id: int
    comment: str
    authod_id: int
    date_created: datetime.datetime

