from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr = Field(..., title="user email address")


class UserCreate(UserBase):
    username: str = Field(..., title="user username")
    password: str = Field(..., title = 'user password')


class User(UserBase):
    id: int
    is_active: bool
    is_verified: bool

    class Config:
        orm_mode = True


class OTP(BaseModel):
    user_id: int
    code: Optional[str] = None


    class Config:
        orm_mode = True

class OneTimePassword(BaseModel):
    code : str