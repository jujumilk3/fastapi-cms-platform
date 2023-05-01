from pydantic import Field
from pydantic.main import BaseModel
from sqlalchemy import Boolean, Column, Integer, String

from app.core.constant import ContentType
from app.model.base_model import ArrayType, Base, CustomPydanticBaseModel, ModelBaseInfoDto


class Comment(Base):
    user_token: str = Column(String, nullable=False)
    content: str = Column(String, default="", nullable=False)
    images: list[str] = Column(ArrayType(), nullable=True)
    mention_tokens: list[str] = Column(ArrayType(), nullable=True)
    parent_comment_id: int = Column(Integer, default=None, nullable=True)
    is_deleted: bool = Column(Boolean, default=False, nullable=False)

    content_id: int = Column(Integer, nullable=False)
    content_type: ContentType = Column(String, nullable=False)


class CommentDto:
    class Base(CustomPydanticBaseModel):
        content: str = Field(default=None, description="content", example="content")
        images: list[str] = Field(default=None, description="images", example=["image_url"])
        mention_tokens: list[str] = Field(default=None, description="mention_tokens", example=["mention_token"])
        parent_comment_id: int = Field(default=None, description="parent_comment_id", example=1)
        is_deleted: bool = Field(default=False, description="is_deleted", example=False)
        content_id: int = Field(default=None, description="content_id", example=1)
        content_type: ContentType = Field(default=None, description="content_type", example="post")

    class WithModelBaseInfo(ModelBaseInfoDto, Base):
        user_token: str = Field(default=None, description="user_token", example="user_token")
        reaction_count: int = Field(default=None, description="reaction_count", example=1)

    class Upsert(Base):
        ...

    class UpsertWithUserToken(Upsert):
        user_token: str = Field(default=None, description="user_token", example="user_token")

    class ListResponse(BaseModel):
        results: list["CommentDto.WithModelBaseInfo"] = Field(default=None, description="items", example=[])


CommentDto.ListResponse.update_forward_refs()
