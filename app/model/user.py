from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, DateTime, String

from app.model.base_model import Base


class User(Base):
    email: str = Column(String, nullable=False, comment="email")
    password: str = Column(String, nullable=False, comment="password")
    nickname: str = Column(String, nullable=False, comment="nickname", default="")
    profile_image_url: str = Column(String, nullable=False, comment="profile_image_url", default="")
    user_token: str = Column(String, nullable=False, comment="user_token")
    is_active: bool = Column(Boolean, nullable=False, comment="is_active")
    is_superuser: bool = Column(Boolean, nullable=False, comment="is_superuser")
    is_verified: bool = Column(Boolean, nullable=False, comment="is_verified")
    is_deleted: bool = Column(Boolean, nullable=False, comment="is_deleted")
    visited_at: datetime = Column(
        DateTime, nullable=False, comment="last_login_at", default=datetime.utcnow, onupdate=datetime.utcnow
    )


class UserDto(BaseModel):
    id: int = Field(default=None, title="id", description="id")
    created_at: datetime = Field(default=None, title="created_at", description="created_at")
    updated_at: datetime = Field(default=None, title="updated_at", description="updated_at")
    email: str = Field(default=None, title="email", description="email")
    password: str = Field(default=None, title="password", description="password")
    nickname: str = Field(default=None, title="nickname", description="nickname")
    profile_image_url: str = Field(default=None, title="profile_image_url", description="profile_image_url")
    user_token: str = Field(default=None, title="user_token", description="user_token")
    is_active: bool = Field(default=None, title="is_active", description="is_active")
    is_superuser: bool = Field(default=None, title="is_superuser", description="is_superuser")
    is_verified: bool = Field(default=None, title="is_verified", description="is_verified")
    is_deleted: bool = Field(default=None, title="is_deleted", description="is_deleted")
    visited_at: datetime = Field(default=None, title="last_login_at", description="last_login_at")


class UserBaseInfoDto(BaseModel):
    email: str = Field(..., title="email", description="email")
    nickname: str = Field(..., title="nickname", description="nickname")
    user_token: str = Field(..., title="user_token", description="user_token")
    profile_image_url: str = Field(..., title="profile_image_url", description="profile_image_url")


class AuthDto:
    class Payload(BaseModel):
        email: str
        nickname: str
        user_token: str

    class JWTPayload(BaseModel):
        email: str
        nickname: str
        user_token: str
        access_token: str
        expiration: int

    class SignUp(BaseModel):
        email: str = Field(nullable=False, example="test@test.com")
        password: str = Field(nullable=False, example="test1234")
        nickname: str = Field(nullable=False, example="testnickname")

    class SignIn(BaseModel):
        email: str = Field(nullable=False, example="test@test.com")
        password: str = Field(nullable=False, example="test1234")

    class SignInResponse(BaseModel):
        access_token: str
        expiration: int
        user_info: UserBaseInfoDto
