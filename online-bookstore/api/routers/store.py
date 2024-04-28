from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import database, models
from ..schemas import book_schemas


router = APIRouter(prefix="/store", tags=["Book store"])


@router.get("/")
def get_all_books(db: Session = Depends(database.get_db)):
    books = db.query(models.Book).all()
    return books

@router.get("/{id}")
def get_single_book(id: int, db: Session = Depends(database.get_db)):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=book_schemas.Book)
def create_book(book: book_schemas.Book, db: Session = Depends(database.get_db)):
    book = models.Book(**book.dict())

    db.add(book)
    db.commit()
    db.refresh(book)
    return book