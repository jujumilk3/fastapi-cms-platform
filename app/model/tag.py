from pydantic import Field
from pydantic.main import BaseModel
from sqlalchemy import Column, String

from app.model.base_model import Base, CustomPydanticBaseModel, ModelBaseInfoDto


class Tag(Base):
    user_token: str = Column(String, nullable=False, comment="user_token")
    tag: str = Column(String, nullable=False, comment="tag")


class TagDto:
    class Base(CustomPydanticBaseModel):
        user_token: str = Field(default=None, description="user_token", example="user_token")
        tag: str = Field(default=None, description="tag", example="tag")

    class WithModelBaseInfo(ModelBaseInfoDto, Base):
        ...

    class Upsert(Base):
        ...

    class ListResponse(BaseModel):
        results: list["TagDto.WithModelBaseInfo"] = Field(default=None, description="items", example=[])


TagDto.ListResponse.update_forward_refs()
