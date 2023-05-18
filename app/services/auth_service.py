from datetime import timedelta

from app.core.config import configs
from app.core.exception import AuthError
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import AuthDto, User, UserDto
from app.repositories.user_repository import UserRepository
from app.services.base_service import BaseService
from app.utils.common import random_hash


class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    async def sign_in(self, sign_in_dto: AuthDto.SignIn):
        found_user = await self.user_repository.select_user_by_email(sign_in_dto.email)
        if not found_user:
            raise AuthError(detail="Incorrect email or password")
        if not verify_password(sign_in_dto.password, found_user.password):
            raise AuthError(detail="Incorrect email or password")
        if not found_user.is_active:
            raise AuthError(detail="Account is not active")
        payload = AuthDto.Payload(**found_user.dict())
        token_lifespan = timedelta(seconds=configs.JWT_ACCESS_EXPIRE)
        jwt = create_access_token(payload, token_lifespan)
        return AuthDto.JWTPayload(access_token=jwt["access_token"], exp=jwt["exp"], **payload.dict())

    async def sign_up(self, sing_up_dto: AuthDto.SignUp) -> AuthDto.JWTPayload:
        user_token = random_hash(length=12)
        user = User(
            **sing_up_dto.dict(exclude_none=True),
            is_active=True,
            is_superuser=False,
            is_deleted=False,
            is_verified=False,
            user_token=user_token
        )
        user.password = get_password_hash(sing_up_dto.password)
        created_user = await self.user_repository.insert(user)
        payload = AuthDto.Payload(**created_user.dict())
        token_lifespan = timedelta(seconds=configs.JWT_ACCESS_EXPIRE)
        jwt = create_access_token(payload, token_lifespan)
        return AuthDto.JWTPayload(access_token=jwt["access_token"], exp=jwt["exp"], **payload.dict())

    async def change_password(self, old_password: str, new_password: str, new_password_confirm: str, user_token: str):
        found_user = await self.user_repository.select_user_by_user_token(user_token)
        if not found_user:
            raise AuthError(detail="User not found")
        if not verify_password(old_password, found_user.password):
            raise AuthError(detail="Incorrect old password")
        if new_password != new_password_confirm:
            raise AuthError(detail="New password and new password confirm not match")
        updated_user = await self.user_repository.update(
            found_user.id, UserDto.Upsert(password=get_password_hash(new_password))
        )
        payload = AuthDto.Payload(**updated_user.dict())
        token_lifespan = timedelta(seconds=configs.JWT_ACCESS_EXPIRE)
        jwt = create_access_token(payload, token_lifespan)
        return AuthDto.JWTPayload(access_token=jwt["access_token"], exp=jwt["exp"], **payload.dict())
