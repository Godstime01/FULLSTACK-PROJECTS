from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import models


def check_user_exist(email, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    
    return user