from passlib.context import CryptContext
# from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from fastapi import BackgroundTasks
import pyotp
from typing import List
from .config import get_settings

settings = get_settings()
secret_key = pyotp.random_base32()
time_otp = pyotp.TOTP(secret_key, interval=120)

pwd_context = CryptContext(schemes=['bcrypt'])

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def generate_otp_code():
    otp = time_otp.now()

def verify_otp(code):
    return time_otp.verify(code)


# conf = ConnectionConfig(
#     MAIL_USERNAME = f'{settings.email_username}',
#     MAIL_PASSWORD = f'{settings.email_password}',
#     MAIL_FROM = f'{settings.email_from}',
#     MAIL_PORT = f"{settings.port}",
#     MAIL_SERVER = f'{settings.mail_server}',
#     MAIL_STARTTLS = False,
#     MAIL_SSL_TLS = True,
#     USE_CREDENTIALS = True,
#     VALIDATE_CERTS = True
# )

def send_email(background_task: BackgroundTasks, subject: str, recipient: List, message: str):
    # mail = FastMail(conf)
    # msg = MessageSchema(
    #     subject = subject,
    #     recipients = recipient,
    #     body = message,
    #     subtype = MessageType.html
    # )

    # background_task.add_task(mail.send_message, msg)
    pass