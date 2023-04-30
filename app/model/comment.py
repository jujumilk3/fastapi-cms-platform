from pydantic import Field
from pydantic.main import BaseModel
from sqlalchemy import Column

from app.core.constant import ContentType
from app.model.base_model import ArrayType, Base, ModelBaseInfoDto, CustomPydanticBaseModel


class Comment(Base):
    user_token: str = Field(nullable=False)
    content: str = Field(default="", nullable=False)
    images: list[str] = Field(default="", sa_column=Column(ArrayType()), nullable=False)
    mention_tokens: list[str] = Field(default=None, sa_column=Column(ArrayType()))
    parent_comment_id: int = Field(default=None, nullable=True)
    is_deleted: bool = Field(default=False, nullable=False)

    content_id: int = Field(nullable=False)
    content_type: ContentType = Field(nullable=False)


class CommentDto:
    class Base(CustomPydanticBaseModel):
        user_token: str = Field(default=None, description="user_token", example="user_token")
        content: str = Field(default=None, description="content", example="content")
        images: list[str] = Field(default=None, description="images", example=["image_url"])
        mention_tokens: list[str] = Field(default=None, description="mention_tokens", example=["mention_token"])
        parent_comment_id: int = Field(default=None, description="parent_comment_id", example=1)
        is_deleted: bool = Field(default=None, description="is_deleted", example=False)
        content_id: int = Field(default=None, description="content_id", example=1)
        content_type: ContentType = Field(default=None, description="content_type", example="post")

    class WithModelBaseInfo(ModelBaseInfoDto, Base):
        ...

    class Upsert(Base):
        ...

    class ListResponse(BaseModel):
        results: list["CommentDto.WithModelBaseInfo"] = Field(default=None, description="items", example=[])


CommentDto.ListResponse.update_forward_refs()
