from fastapi import Response, HTTPException
from app.dto.auth_dto import AuthDto, AuthResponseDto
from app.services.base_service import BaseService
from app.core.security import (
    hash_password,
    create_access_token,
    create_refresh_token,
    verify_password,
    ACCESS_TOKEN_COOKIE_NAME,
    REFRESH_TOKEN_COOKIE_NAME,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES
    )


class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository = UserRepository()):
        self.user_repository = user_repository

    async def _set_token_cookie(response: Response, access_token: str, refresh_token: str):
        response.set_cookie(
            key=ACCESS_TOKEN_COOKIE_NAME,
            value=access_token,
            httponly=True,
            samesite="none",  # "lax" for production
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            path="/"
        )
        response.set_cookie(
            key=REFRESH_TOKEN_COOKIE_NAME,
            value=refresh_token,
            httponly=True,
            secure=False,  # True for production
            samesite="none",  # "lax" for production
            max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
            path="/"
        )

    async def register(self, data: AuthDto, response: Response) -> AuthResponseDto:
        existing_user = await self.user_repository.find_by_email(data.email)

        if existing_user:
            raise HTTPException(status_code=401, detail="Email already registered")
        
        hashed_password = hash_password(data.password)
        data.password = hashed_password
        user = await self.user_repository.create(data)

        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        await self._set_token_cookie(response, access_token, refresh_token)

        return AuthResponseDto(
            access_token=access_token
        )
    
    async def login(self, data: AuthDto, response: Response) -> AuthResponseDto:
        user = await self.user_repository.find_by_email(data.email)

        if not user:
            raise HTTPException(status_code=401, detail="User with this Email does not exist")

        if not verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        await self._set_token_cookie(response, access_token, refresh_token)

        return AuthResponseDto(
            access_token=access_token
        )