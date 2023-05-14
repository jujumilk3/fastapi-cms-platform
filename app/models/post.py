from pydantic import Field
from pydantic.main import BaseModel
from sqlalchemy import Boolean, Column, Integer, String

from app.core.constant import Language
from app.models.base_model import Base, CustomPydanticBaseModel, ModelBaseInfoDto


class Post(Base):
    title: str = Column(String, nullable=False, comment="title")
    content: str = Column(String, nullable=False, comment="content")
    user_token: str = Column(String, nullable=False, comment="user_token")
    language: Language = Column(String, nullable=False, comment="language")
    reaction_count: int = Column(Integer, default=0, nullable=False, comment="reaction_count")
    comment_count: int = Column(Integer, default=0, nullable=False, comment="comment_count")

    is_notice: bool = Column(Boolean, nullable=False, comment="is_notice")
    is_deleted: bool = Column(Boolean, nullable=False, comment="is_deleted")
    is_published: bool = Column(Boolean, nullable=False, comment="is_published")
    is_private: bool = Column(Boolean, nullable=False, comment="is_private")

    board_id: int = Column(Integer, nullable=True, comment="board_id")


class PostDto:
    class Base(CustomPydanticBaseModel):
        title: str = Field(default=None, description="post title", example="title")
        content: str = Field(default=None, description="post content", example="content")
        language: Language = Field(default=None, description="language", example="ko")

        is_notice: bool = Field(default=False, description="is_notice", example=False)
        is_deleted: bool = Field(default=None, description="is_deleted", example=False)
        is_published: bool = Field(default=None, description="is_published", example=True)
        is_private: bool = Field(default=None, description="is_private", example=False)

        board_id: int = Field(default=None, description="board_id", example=1)

    class WithModelBaseInfo(ModelBaseInfoDto, Base):
        user_token: str = Field(default=None, description="user_token", example="user_token")
        reaction_count: int = Field(default=0, description="reaction_count", example=0)
        comment_count: int = Field(default=0, description="comment_count", example=0)

    class Upsert(Base):
        ...

    class UpsertWithUserToken(Upsert):
        user_token: str = Field(default=None, description="user_token", example="user_token")

    class UpsertFeedWithBoardManageName(Upsert):
        board_manage_name: str = Field(default=None, description="board_manage_name", example="free")

    class ListResponse(BaseModel):
        results: list["PostDto.WithModelBaseInfo"] = Field(default=None, description="items", example=[])


PostDto.ListResponse.update_forward_refs()
