from pydantic import Field
from pydantic.main import BaseModel
from sqlalchemy import Boolean, Column, String, Integer

from app.model.base_model import Base, ListResponseDto, ModelBaseInfoDto


class Bookmark(Base):
    user_token: str = Column(String(255), nullable=False, index=True)
    content_id: int = Column(Integer, nullable=False, index=True)
    content_type: str = Column(String(255), nullable=False, index=True)


class BookmarkDto:
    class Base(BaseModel):
        user_token: str = Field(default=None, description="user_token", example="user_token")
        content_id: int = Field(default=None, description="content_id", example=1)
        content_type: str = Field(default=None, description="content_type", example="post")

    class WithModelBaseInfo(ModelBaseInfoDto, Base):
        ...

    class Upsert(Base):
        ...

    class ListResponse(ListResponseDto):
        results: list["BookmarkDto.WithModelBaseInfo"] = Field(default=None, description="items", example=[])


BookmarkDto.ListResponse.update_forward_refs()
