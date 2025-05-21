from fastapi import APIRouter, Request, Response, Depends, status
from app.dto.auth_dto import AuthDto, AuthResponseDto
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])

def get_auth_service() -> AuthService:
    return AuthService()

@router.post('/register', response_model=AuthResponseDto, status_code=status.HTTP_201_CREATED)
async def register(
    data: AuthDto,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service)
    ) -> AuthResponseDto:
    result: AuthResponseDto = await auth_service.register(data, response)
    return result

@router.post("/login")
async def login(
    data: AuthDto,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service)
    ) -> AuthResponseDto:
    result: AuthResponseDto = await auth_service.login(data, response)
    return result

@router.post('/login/access-token', response_model=AuthResponseDto, status_code=status.HTTP_200_OK)
async def login_access_token(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service)
    ) -> AuthResponseDto:
    result: AuthResponseDto = await auth_service.login_access(request, response)
    return result

@router.post('/logout')
async def logout(
    response: Response,
    auth_service: AuthService = Depends(get_auth_service)
    ) -> bool:
    await auth_service.logout(response)
    return True
