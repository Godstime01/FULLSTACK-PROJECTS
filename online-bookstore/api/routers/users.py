from fastapi import APIRouter, Depends , HTTPException, status
from sqlalchemy.orm import Session
from ..database import database, models, _query
from .. import utils


from ..schemas import user_schemas as sc

router = APIRouter(prefix="/auth", tags=["User and Authentication"])


@router.post("/login")
def login_user(user, db: Session = Depends(database.get_db)):

    # check if user email exist
    result = _query.check_user_exist(user.email, db)

    if not result:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    
    # verify password hash
    valid_password = utils.verify_password(user.password, result.password)

    if not valid_password:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    
    # genreate jwt token

    return {
        "message": "your login was successful",
    }


@router.post("/register", response_model=sc.UserCreated)
def register_user(user: sc.User, db: Session = Depends(database.get_db)):

    # check if user email exist
    result = _query.check_user_exist(user.email, db)

    if result: raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="user email already exist")

    # hash password
    user.password = utils.hash_password(user.password)
    # create new user
    new_user = models.User(
        username=user.username, email=user.email, password=user.password
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/reset-password")
def reset_password():
    return


@router.get("/verify-user")
def verify_user():
    return
