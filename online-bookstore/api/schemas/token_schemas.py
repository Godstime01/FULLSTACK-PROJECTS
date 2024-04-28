from pydantic import BaseConfig


class TokenResponse(BaseConfig):
    exp: str
    access_token : str
    refresh_token: str
    