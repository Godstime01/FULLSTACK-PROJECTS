from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """data schema used to create a user"""    
    
    username: str
    email: EmailStr
    password: str
    # is_verified: bool = False


class UserCreated(BaseModel):
    """data schema used to after creating a user"""    
    
    username: str
    email: EmailStr
    is_verified: bool


