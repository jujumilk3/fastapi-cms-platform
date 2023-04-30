from pydantic import Field
from pydantic.main import BaseModel
from sqlalchemy import Boolean, Column, String

from app.model.base_model import Base, ListResponseDto, ModelBaseInfoDto


class Board(Base):
    display_name: str = Column(String, nullable=False, comment="display_name")
    manage_name: str = Column(String, nullable=False, comment="manage_name", unique=True)
    is_published: bool = Column(Boolean, nullable=False, comment="is_published")
    is_admin_only: bool = Column(Boolean, nullable=False, comment="is_admin_only")
    description: str = Column(String, nullable=False, comment="description")
    main_image: str = Column(String, nullable=False, comment="main_image")
    background_image: str = Column(String, nullable=False, comment="background_image")


class BoardDto:
    class Base(BaseModel):
        display_name: str = Field(default=None, description="board display name", example="free")
        manage_name: str = Field(default=None, description="board manage name for internal managing", example="free")
        is_published: bool = Field(default=None, description="board is published", example=True)
        is_admin_only: bool = Field(default=None, description="board is admin only", example=False)
        description: str = Field(default=None, description="board description", example="it's free board")
        main_image: str = Field(default=None, description="board main image", example="https://image.com/image.png")
        background_image: str = Field(
            default=None, description="board background image", example="https://image.com/image.png"
        )

        class Config:
            orm_mode = True

    class WithModelBaseInfo(ModelBaseInfoDto, Base):
        ...

    class Upsert(Base):
        ...

    class ListResponse(ListResponseDto):
        results: list["BoardDto.WithModelBaseInfo"] = Field(default=None, description="items", example=[])


BoardDto.ListResponse.update_forward_refs()
