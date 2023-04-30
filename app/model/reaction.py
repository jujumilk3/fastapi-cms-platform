from pydantic import Field
from pydantic.main import BaseModel
from sqlalchemy import Column, Integer, String

from app.core.constant import ContentType, ReactionType
from app.model.base_model import Base, CustomPydanticBaseModel, ModelBaseInfoDto


class Reaction(Base):
    user_token: str = Column(String, nullable=False, comment="user_token")
    content_id: int = Column(Integer, nullable=False, comment="content_id")
    content_type: ContentType = Column(String, nullable=False, comment="content_type")
    reaction_type: ReactionType = Column(String, nullable=False, comment="reaction_type")
    unique_key: str = Column(String, nullable=True, unique=True, comment="unique_key")


class ReactionDto:
    class Base(CustomPydanticBaseModel):
        user_token: str = Field(default=None, description="user_token", example="user_token")
        content_id: int = Field(default=None, description="content_id", example=1)
        content_type: ContentType = Field(default=None, description="content_type", example="post")
        reaction_type: ReactionType = Field(default=None, description="reaction_type", example="like")
        unique_key: str = Field(default=None, description="unique_key", example="post_1_like_user_token")

    class WithModelBaseInfo(ModelBaseInfoDto, Base):
        ...

    class Upsert(Base):
        ...

    class ListResponse(BaseModel):
        results: list["ReactionDto.WithModelBaseInfo"] = Field(default=None, description="items", example=[])


ReactionDto.ListResponse.update_forward_refs()
