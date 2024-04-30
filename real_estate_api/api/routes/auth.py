from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks, Response
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schema, utils, _query
from .. import models

router = APIRouter(
    prefix="/api/v1/auth",
    tags=['User Authentication']
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: schema.UserCreate, background_task:BackgroundTasks, db: Session = Depends(get_db)): 

    # check if user email exist
    result = _query.check_user_exist(db, user.email)

    if result: raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="user email already exist")

    # hash password
    user.password = utils.hash_password(user.password)
    # create new user
    result = _query.insert_new_user(db, user)

    # return result

    # send email notification
    otp_code = utils.generate_otp_code()
    otp_data = schema.OTP
    otp_data.code = otp_code
    otp_data.user_id = result.id
    
    message = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OTP Verification</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f0f0f0;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background-color: #ffffff; padding: 40px;">
            <h2 style="font-size: 24px; margin-bottom: 20px;">OTP Verification</h2>
            <p style="font-size: 16px; margin-bottom: 20px;">Thank you for signing up! Please use the following OTP (One-Time Password) to verify your email {0:}:</p>
            <p style="font-size: 20px; font-weight: bold; margin-bottom: 20px;">{1:}</p>
            <p style="font-size: 14px; margin-bottom: 10px;">This OTP is valid for a short period of time. Please do not share it with anyone.</p>
        </div>
    </div>
</body>
</html>
    """.format(user.email, otp_code)

    utils.send_email(background_task = background_task, subject="Email Verification", recipient=[user.email], message=message )

    _query.create_otp_for_user(db, otp=otp_data)

    return { 
        "message": "account created successfully, please verify with your one time password"
    } 


@router.post("/email-verification", status_code = status.HTTP_200_OK)
async def verify_email(otp: schema.OneTimePassword, response: Response, db: Session = Depends(get_db)):
    otp_user_qs = db.query(models.User_otp).filter(models.User_otp.code == otp.code)

    otp_user = otp_user_qs.first()

    isValid = utils.verify_otp(otp.code)

    if isValid and otp_user.is_valid:
        user_qs = db.query(models.User).filter(models.User.id == otp_user.user_id)

        user = user_qs.first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "invalid otp")
        
        user_qs.update({"is_verified":True} , synchronize_session=True)
        otp_user_qs.update({"is_valid":False}, synchronize_session=True)

        return {
            "status": "account verified sucessfully",
            "is_verified": user.is_verified
        }

    else:
        otp_user_qs.update({"is_valid":False}, synchronize_session=False)
        response.status_code = status.HTTP_400_BAD_REQUEST

        return {
            "message": "invalide otp or otp has expired",
        }