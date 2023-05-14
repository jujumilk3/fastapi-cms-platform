from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status

from app.core.container import Container
from app.core.dependency import get_current_active_user_token
from app.models.user import AuthDto, User, UserDto
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/change-password", response_model=AuthDto.JWTPayload, status_code=status.HTTP_200_OK)
@inject
async def change_password(
    old_password: str = Body(..., description="Old password"),
    new_password: str = Body(..., description="New password"),
    new_password_confirm: str = Body(..., description="New password confirm"),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
    user_token: str = Depends(get_current_active_user_token),
):
    return await auth_service.change_password(
        old_password=old_password,
        new_password=new_password,
        new_password_confirm=new_password_confirm,
        user_token=user_token,
    )


@router.patch("/change-profile", status_code=status.HTTP_200_OK)
@inject
async def change_profile(
    self_updatable_attributes: UserDto.SelfUpdatableAttributes,
    *,
    user_service: UserService = Depends(Provide[Container.user_service]),
    user_token: str = Depends(get_current_active_user_token),
):
    return await user_service.patch_user_profile_after_check_user_token(self_updatable_attributes, user_token)
