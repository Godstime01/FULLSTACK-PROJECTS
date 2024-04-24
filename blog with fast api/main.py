from fastapi import FastAPI, HTTPException, Depends, status, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm


import models
import schemas
from database import SessionLocal, engine, get_db
import utils


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


@app.get("/blog/", status_code=status.HTTP_200_OK, tags=["blog"])
def get_all_post(db: Session = Depends(get_db)):
    blogs = db.query(models.Post).all()

    return blogs


@app.post("/blog/", status_code=status.HTTP_200_OK, tags=["blog"])
def create_post(request: schemas.Post, db: Session = Depends(get_db)):
    new_blog = models.Post(**request.dict())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.put("/update-post/{title}/", status_code=status.HTTP_202_ACCEPTED, tags=["blog"])
def update_post(title, request: schemas.Post, db: Session = Depends(get_db)):
    (
        db.query(models.Post)
        .filter(models.Post.title == title)
        .update(request.dict(), synchronize_session=False)
    )
    db.commit()
    return


@app.delete(
    "/delete-post/{title}/", status_code=status.HTTP_204_NO_CONTENT, tags=["blog"]
)
def delete_post(title, db: Session = Depends(get_db)):
    post = (
        db.query(models.Post)
        .filter(models.Post.title == title)
        .delete(synchronize_session=False)
    )


@app.get("/blog/{title}/", status_code=status.HTTP_200_OK, tags=["blog"])
def get_single_blog(title, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.title == title).first()

    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"There's not post with the title {title}"
        )

    return post


# comment
@app.post(
    "/blog/{post_id}/comments/", status_code=status.HTTP_201_CREATED, tags=["comment"]
)
def post_comment(post_id: int, request: schemas.Comment, db: Session = Depends(get_db)):

    # Check if the post with the given post_id exists
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Create a new comment associated with the post
    comment_data = request.dict()
    comment_data["post_id"] = post_id
    comment = models.Comment(**comment_data)

    # Add the comment to the database
    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


@app.get("/blog/{post_id}/comments/", status_code=status.HTTP_200_OK, tags=["comment"])
def get_post_comment(post_id: int, db: Session = Depends(get_db)):
    # Check if the post with the given post_id exists
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Query comments for the post with pagination
    comments = db.query(models.Comment).filter(models.Comment.post_id == post_id).all()

    return comments


@app.post(
    "/sign-up/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOutput,
    tags=["users"],
)
def register(request: schemas.User, db: Session = Depends(get_db)):

    # get password and hash it
    hashed_password = utils.hash_password(request.password)

    # create new user
    new_user = models.User(
        username=request.username, email=request.email, password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/user/{id}/", status_code=status.HTTP_200_OK, tags=["users"], response_model=schemas.UserOutput)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There's no user with that {id}",
        )

    return user

@app.post("/login/", status_code=status.HTTP_200_OK, tags=['users'])
def login(request: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail='The User does not exist')
    
    if not utils.verify_password(request.password, user.password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail='The User password does not match')
    
    access_token = utils.create_access_token(data={"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}