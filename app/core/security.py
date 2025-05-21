import bcrypt
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta

from app.core.configs import Config


JWT_SECRET_KEY = Config.get_env("JWT_SECRET_KEY")
ALGORITHM = Config.get_env("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(Config.get_env("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(Config.get_env("REFRESH_TOKEN_EXPIRE_DAYS")) * 24 * 60
ACCESS_TOKEN_COOKIE_NAME = 'access_token'
REFRESH_TOKEN_COOKIE_NAME = 'refresh_token'

def create_token(data: dict, _timedelta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + _timedelta
    to_encode.update({"exp": expire})
    return jwt.encode(data, JWT_SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(data: dict):
    return create_token(data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(data: dict):
    return create_token(data, timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))

def decode_token(token: str):
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])

def hash_password(password: str) -> str:
    return bcrypt.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)
