from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..config import get_settings


settings = get_settings()

# SQLALCHEMY_DATABASE_URL = "sqlite:///./bookstore.sqlite3"
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL



engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
