import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = Path(".env")
print(env_path)
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_PORT: str = os.getenv("DB_POST")
    DATABASE_URL : str = os.getenv("DB_DATABASE_URL")


    SECRET_KEY : str = os.getenv("SECRET_KEY")
    ALGORITHM  : str = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES : str = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


def get_settings():
    return Settings()


get_settings()