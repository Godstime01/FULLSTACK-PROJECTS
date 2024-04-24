from fastapi import FastAPI, HTTPException, Depends, status, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session


import models
import schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)  # makes migrations to all tables

app = FastAPI()

# Define CORS settings
origins = ["*"]  # Allow requests from any origin

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/blog/")
def get_all_post(db: Session = Depends(get_db)):
    blogs = db.query(models.Post).all()

    return blogs


@app.post("/blog/", status_code=status.HTTP_200_OK)
def create_post(request: schemas.Post, db: Session = Depends(get_db)):
    new_blog = models.Post(**request.dict())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.put("/update-post/{title}/", status_code=status.HTTP_202_ACCEPTED)
def update_post(title, request: schemas.Post, db: Session = Depends(get_db)):
    (
        db.query(models.Post)
        .filter(models.Post.title == title)
        .update(request.dict(), synchronize_session=False)
    )
    db.commit()
    return


@app.delete("/delete-post/{title}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(title, db: Session = Depends(get_db)):
    post = (
        db.query(models.Post)
        .filter(models.Post.title == title)
        .delete(synchronize_session=False)
    )


@app.get("/blog/{title}/", status_code=status.HTTP_200_OK)
def get_single_blog(title, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.title == title).first()

    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"There's not post with the title {title}"
        )

    return post
