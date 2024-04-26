import pathlib
from pydantic import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    # db_host:str 
    # db_port:str
    # db_username:str
    # db_password:str
    # db_name:str

    email_username :str
    email_password :str
    email_from: str
    mail_server: str

    class Config:
        env_file = f"{pathlib.Path(__file__).resolve().parent}/.env"

def get_settings():
    return Settings()
    
get_settings()

