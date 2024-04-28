from sqlalchemy import Column, Integer, String, Boolean, DATETIME
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(12))
    email = Column(String, unique=True)
    password = Column(String)
    is_verified = Column(Boolean, default=False)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key= True, autoincrement=True, index = True)
    title = Column(String, index=True, unique=True)
    # description = Column(String)
    author = Column(String)

    # date_added = Column(DATETIME, )