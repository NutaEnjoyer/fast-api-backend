from pydantic import BaseModel, EmailStr


class AuthDto(BaseModel):
    email: EmailStr
    password: str


class AuthResponseDto(BaseModel):
    access_token: str
