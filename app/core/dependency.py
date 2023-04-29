from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from jose import jwt
from pydantic import ValidationError

from app.core.config import config
from app.core.container import Container
from app.core.exception import AuthError, ForbiddenError
from app.core.security import JWTBearer
from app.model.user import AuthDto, User
from app.service.user_service import UserService


async def get_current_user_token(
    bearer_token: str = Depends(JWTBearer(auto_error=False)),
) -> str:
    try:
        decoded = jwt.decode(bearer_token, config.JWT_SECRET_KEY, algorithms=config.JWT_ALGORITHM)
        payload = AuthDto.Payload(**decoded)
    except (jwt.JWTError, ValidationError, AttributeError) as e:
        raise AuthError(detail="Could not validate credentials") from e
    return payload.user_token


@inject
async def get_current_active_user_token(
    user_token: str = Depends(get_current_user_token),
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> str:
    current_user: User = await user_service.get_user_by_user_token(user_token=user_token)
    if not current_user:
        raise AuthError(detail="User not found")
    current_user.password = "***"
    if not current_user.is_active:
        raise AuthError("Inactive user")
    return current_user.user_token


async def get_current_user_token_no_exception(
    bearer_token: str = Depends(JWTBearer(auto_error=False)),
) -> str:
    try:
        decoded = jwt.decode(bearer_token, config.JWT_SECRET_KEY, algorithms=config.JWT_ALGORITHM)
        payload = AuthDto.Payload(**decoded)
    except (jwt.JWTError, ValidationError, AttributeError):
        return ""
    return payload.user_token


@inject
async def get_current_super_user(
    user_token: str = Depends(get_current_user_token),
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> User:
    current_user: User = await user_service.get_user_by_user_token(user_token=user_token)
    if not current_user:
        raise AuthError("User not found")
    if not current_user.is_active:
        raise AuthError("Inactive user")
    if not current_user.is_superuser:
        raise ForbiddenError("It's not a super user")
    return current_user
