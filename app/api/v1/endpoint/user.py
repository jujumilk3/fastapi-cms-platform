from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status

from app.core.container import Container
from app.core.dependency import get_current_active_user_token
from app.model.user import AuthDto, User
from app.service.auth_service import AuthService
from app.service.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/change-password", status_code=status.HTTP_200_OK)
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
