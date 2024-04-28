from fastapi import FastAPI

from .routers import users
from .routers import store
from .database import database

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)  # makes migrations to all tables

app.include_router(users.router)
app.include_router(store.router)
# app.include_router()

@app.get('/')
def testing():
    return {"ping": "pong"}


