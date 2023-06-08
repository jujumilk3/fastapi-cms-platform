from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container
from app.core.dependency import get_current_active_user_token, get_current_user_payload, get_current_user_token
from app.models.user import AuthDto, User, UserDto
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/signin", response_model=AuthDto.JWTPayload, status_code=status.HTTP_200_OK)
@inject
async def sign_in(
    user_info: AuthDto.SignIn,
    *,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    return await auth_service.sign_in(user_info)


@router.post("/signup", response_model=AuthDto.JWTPayload, status_code=status.HTTP_201_CREATED)
@inject
async def sign_up(
    user_info: AuthDto.SignUp,
    *,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    return await auth_service.sign_up(user_info)


@router.get("/me", response_model=UserDto.Base, status_code=status.HTTP_200_OK)
@inject
async def get_me(
    user_token: str = Depends(get_current_active_user_token),
    *,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    me: User = await user_service.get_user_by_user_token(user_token=user_token)
    me.password = "***"
    user_dto = UserDto.Base(**me.dict())
    return user_dto


@router.post("/refresh", response_model=AuthDto.JWTPayload, status_code=status.HTTP_200_OK)
@inject
async def refresh(
    # It must be take refresh_token from headers.
    # Refer to test_auth_router::test_refresh_token
    payload: AuthDto.Payload = Depends(get_current_user_payload),
    *,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    return await auth_service.build_jwt_payload(payload=payload)
