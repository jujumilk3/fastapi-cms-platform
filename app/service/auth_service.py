from datetime import timedelta

from app.core.config import config
from app.core.exception import AuthError
from app.core.security import create_access_token, get_password_hash, verify_password
from app.model.user import AuthDto, User
from app.repository.user_repository import UserRepository
from app.service.base_service import BaseService
from app.util.common import random_hash


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
        token_lifespan = timedelta(seconds=config.JWT_ACCESS_EXPIRE)
        jwt = create_access_token(payload, token_lifespan)
        return AuthDto.JWTPayload(access_token=jwt["access_token"], expiration=jwt["expiration"], **payload.dict())

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
        token_lifespan = timedelta(seconds=config.JWT_ACCESS_EXPIRE)
        jwt = create_access_token(payload, token_lifespan)
        return AuthDto.JWTPayload(access_token=jwt["access_token"], expiration=jwt["expiration"], **payload.dict())
