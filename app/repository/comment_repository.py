from collections.abc import Callable
from contextlib import AbstractContextManager

from sqlalchemy.ext.asyncio import AsyncSession

from app.model.comment import Comment
from app.repository.base_repository import BaseRepository


class CommentRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[AsyncSession]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Comment)
