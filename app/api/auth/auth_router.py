from fastapi import APIRouter, Response, Depends, status
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

