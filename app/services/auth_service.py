from fastapi import Request, Response, HTTPException
from app.dto.auth_dto import AuthDto, AuthResponseDto
from app.repository.user_repository import UserRepository
from app.services.base_service import BaseService
from app.core.security import (
    decode_token,
    hash_password,
    create_access_token,
    create_refresh_token,
    verify_password,
    REFRESH_TOKEN_COOKIE_NAME,
    REFRESH_TOKEN_EXPIRE_MINUTES
    )


class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository = UserRepository()):
        self.user_repository = user_repository

    def _set_refresh_token_cookie(self, response: Response, refresh_token: str):
        response.set_cookie(
            key=REFRESH_TOKEN_COOKIE_NAME,
            value=refresh_token,
            httponly=True,
            secure=False,  # True for production
            samesite="lax",  # "lax" for production
            max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
            path="/"
        )

    def _remove_refresh_token_cookie(self, response: Response):
        response.delete_cookie(REFRESH_TOKEN_COOKIE_NAME)
    
    async def _get_new_tokens(self, _refresh_token: str) -> tuple[str, str]:
        result = decode_token(_refresh_token)
        if not result: raise HTTPException(status_code=401, detail="Invalid refresh token")

        user = await self.user_repository.find_by_id(result.get("id"))
        if  not user: raise HTTPException(status_code=401, detail="User not found")

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        return access_token, refresh_token

    async def register(self, data: AuthDto, response: Response) -> AuthResponseDto:
        existing_user = await self.user_repository.find_by_email(data.email)

        if existing_user:
            raise HTTPException(status_code=401, detail="Email already registered")
        
        hashed_password = hash_password(data.password)
        data.password = hashed_password
        user = await self.user_repository.create(data)

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        self._set_refresh_token_cookie(response, refresh_token)

        return AuthResponseDto(
            access_token=access_token
        )
    
    async def login(self, data: AuthDto, response: Response) -> AuthResponseDto:
        user = await self.user_repository.find_by_email(data.email)

        if not user:
            raise HTTPException(status_code=401, detail="User with this Email does not exist")

        if not verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        self._set_refresh_token_cookie(response, refresh_token)

        return AuthResponseDto(
            access_token=access_token
        )
    
    async def logout(self, response: Response) -> None:
        self._remove_refresh_token_cookie(response)
    
    async def login_access(self, request: Request, response: Response) -> AuthResponseDto:
        refresh_token = request.cookies.get(REFRESH_TOKEN_COOKIE_NAME)
        if not refresh_token:
            self._remove_refresh_token_cookie(response)
            raise HTTPException(status_code=401, detail="Refresh token not found")

        access_token, refresh_token = await self._get_new_tokens(refresh_token)
        self._set_refresh_token_cookie(response, refresh_token)

        return AuthResponseDto(
            access_token=access_token
        )
    