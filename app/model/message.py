from pydantic import Field
from pydantic.main import BaseModel
from sqlalchemy import Column, Integer, String, Boolean

from app.model.base_model import Base, ListResponseDto, ModelBaseInfoDto


class Message(Base):
    from_user_token: str = Column(String(255), nullable=False, index=True)
    to_user_token: str = Column(String(255), nullable=False, index=True)
    content: str = Column(String(255), nullable=False)
    is_read: bool = Column(Boolean, nullable=False, default=False)
    is_deleted: bool = Column(Boolean, nullable=False, default=False)


class MessageDto:
    class Base(BaseModel):
        to_user_token: str = Field(default=None, description="to_user_token", example="user_token")
        content: str = Field(default=None, description="content", example="content")
        is_read: bool = Field(default=False, description="is_read", example=False)
        is_deleted: bool = Field(default=False, description="is_deleted", example=False)

    class WithModelBaseInfo(ModelBaseInfoDto, Base):
        from_user_token: str = Field(default=None, description="from_user_token", example="user_token")

    class Upsert(Base):
        ...

    class UpsertWithUserToken(Upsert):
        to_user_token: str = Field(default=None, description="to_user_token", example="user_token")

    class ListResponse(ListResponseDto):
        results: list["MessageDto.WithModelBaseInfo"] = Field(default=None, description="items", example=[])


MessageDto.ListResponse.update_forward_refs()
