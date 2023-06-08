from datetime import datetime, timedelta

from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from passlib.context import CryptContext

from app.core.config import configs
from app.core.exception import AuthError
from app.models.user import AuthDto

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(user_info: AuthDto.Payload, expires_delta: timedelta = None) -> dict[str, str]:
    if expires_delta:
        expiration = (datetime.utcnow() + expires_delta).timestamp()
    else:
        expiration = (datetime.utcnow() + timedelta(seconds=configs.JWT_ACCESS_EXPIRE)).timestamp()
    payload = {"exp": int(expiration), **user_info.dict()}
    encoded_jwt = jwt.encode(payload, configs.JWT_SECRET_KEY, algorithm=configs.JWT_ALGORITHM)
    return {"access_token": encoded_jwt, "exp": expiration}


def create_refresh_token(user_info: AuthDto.Payload, expires_delta: timedelta = None) -> dict[str, str]:
    if expires_delta:
        expiration = (datetime.utcnow() + expires_delta).timestamp()
    else:
        expiration = (datetime.utcnow() + timedelta(seconds=configs.JWT_REFRESH_EXPIRE)).timestamp()
    payload = {"exp": int(expiration), **user_info.dict()}
    encoded_jwt = jwt.encode(payload, configs.JWT_SECRET_KEY, algorithm=configs.JWT_ALGORITHM)
    return {"refresh_token": encoded_jwt, "exp": expiration}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, configs.JWT_SECRET_KEY, algorithms=configs.JWT_ALGORITHM)
        return decoded_token if decoded_token["exp"] >= int(round(datetime.utcnow().timestamp())) else None
    except Exception:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise AuthError(detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise AuthError(detail="Invalid token or expired token.")
            return credentials.credentials
        elif self.auto_error:
            raise AuthError(detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = decode_jwt(jwt_token)
        except Exception:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid
