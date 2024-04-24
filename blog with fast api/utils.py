from passlib.context import CryptContext
from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session


import schemas
from database import get_db
import models

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = 'd293c8c2ff8792a59f98a8ab985efa4c073fef2a3c4a534718a3bafea9405463'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password:str):
    """ return a hash password """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "expire": expire.strftime("%Y-%m-%d %H:%M:%S")
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def verify_token_access(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = schemas.TokenData(username=payload.get("sub"))
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(teken: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token_access(teken, credentials_exception)
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if not user:
        raise credentials_exception
    return user