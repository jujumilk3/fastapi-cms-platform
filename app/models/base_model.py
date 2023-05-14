import json
import re
from datetime import datetime

from pydantic import BaseModel
from pydantic.fields import Field
from sqlalchemy import Column, DateTime, Integer, String, TypeDecorator
from sqlalchemy.orm import declarative_base, declared_attr


def resolve_table_name(name: str) -> str:
    names = re.split("(?=[A-Z])", name)
    return "_".join([x.lower() for x in names if x])


class BaseTableModel:
    id: Column = Column(Integer, primary_key=True, index=True)
    created_at: Column = Column(DateTime, default=datetime.utcnow)
    updated_at: Column = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        return resolve_table_name(self.__name__)

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


Base = declarative_base(cls=BaseTableModel)


class CustomPydanticBaseModel(BaseModel):
    class Config:
        orm_mode = True

    def pop(self, key):
        try:
            value = getattr(self, key)
        except AttributeError:
            return None
        delattr(self, key)
        return value


class ModelBaseInfoDto(CustomPydanticBaseModel):
    id: int = Field(default=None, description="id", example=1)
    created_at: datetime = Field(default=None, description="created_at", example="2020-01-01 00:00:00")
    updated_at: datetime = Field(default=None, description="updated_at", example="2020-01-01 00:00:00")


class ListResponseDto(CustomPydanticBaseModel):
    offset: int = Field(default=None, description="offset", example=0)
    limit: int = Field(default=None, description="limit", example=10)
    total: int = Field(default=None, description="total", example=100)
    results: list = Field(default=None, description="items", example=[])


class JsonType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if not value:
            return None
        if isinstance(value, str):
            return json.dumps(value)
        else:
            return value

    def process_result_value(self, value, dialect):
        if not value:
            return None
        if isinstance(value, str):
            return json.loads(value)
        else:
            return value

    def copy(self):
        return JsonType(self.impl.length)


class ArrayType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if not value:
            return ""
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if not value:
            return []
        return json.loads(value)

    def copy(self):
        return ArrayType(self.impl.length)
