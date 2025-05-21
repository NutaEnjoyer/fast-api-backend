import bcrypt
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from app.core.configs import Config


JWT_SECRET_KEY = Config.get_env("JWT_SECRET_KEY")
ALGORITHM = Config.get_env("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(Config.get_env("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(Config.get_env("REFRESH_TOKEN_EXPIRE_DAYS")) * 24 * 60
ACCESS_TOKEN_COOKIE_NAME = 'access_token'
REFRESH_TOKEN_COOKIE_NAME = 'refresh_token'

def create_token(data: dict, _timedelta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + _timedelta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(id: str):
    return create_token({"id": id}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(id: str):
    return create_token({"id": id}, timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))

def decode_token(token: str):
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')         
    salt = bcrypt.gensalt()                              
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)  
    hashed_str = hashed_bytes.decode('utf-8')          
    return hashed_str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)
