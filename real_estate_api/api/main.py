from fastapi import FastAPI
from .routes import auth


app = FastAPI(
    title="Realtor services",
    description="A real estate service api",
    version="0.1.0",
    contact = {
        "name":"Godstime01",
    }
)

@app.get("/")
def testing():
    return {"ping": "pong"}

app.include_router(auth.router)