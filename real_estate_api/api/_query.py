from sqlalchemy.orm import Session
from . import models
from . import schema


def check_user_exist(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user

def insert_new_user(db: Session, user: schema.UserCreate):
    new_user = models.User(email = user.email, password = user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 

def create_otp_for_user(db: Session, otp: Session):
    new_otp = models.User_otp(user_id = otp.user_id, code = otp.code)

    db.add(new_otp)
    db.commit()
    db.refresh(new_otp)
    return new_otp