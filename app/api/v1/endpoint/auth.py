from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container
from app.core.dependency import get_current_active_user_token
from app.model.user import AuthDto, User
from app.service.auth_service import AuthService
from app.service.user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/signin", response_model=AuthDto.JWTPayload, status_code=status.HTTP_200_OK)
@inject
async def sign_in(user_info: AuthDto.SignIn, *, auth_service: AuthService = Depends(Provide[Container.auth_service])):
    return await auth_service.sign_in(user_info)


@router.post("/signup", response_model=AuthDto.JWTPayload, status_code=status.HTTP_201_CREATED)
@inject
async def sign_up(user_info: AuthDto.SignUp, *, auth_service: AuthService = Depends(Provide[Container.auth_service])):
    return await auth_service.sign_up(user_info)


@router.get("/me")
@inject
async def get_me(
    user_token: str = Depends(get_current_active_user_token),
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    me: User = await user_service.get_user_by_user_token(user_token=user_token)
    me.password = "***"
    return me
