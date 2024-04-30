import sqlalchemy as sql
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    # date_joined = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    user_otp = relationship("User_otp", back_populates="user")


class User_otp(Base):
    __tablename__ = "user_otp"
    
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="user_otp")
    code = Column(String(6), unique=True, nullable=False)
    is_valid = Column(Boolean, default=True)