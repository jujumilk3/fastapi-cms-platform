from collections.abc import Callable
from contextlib import AbstractContextManager

from sqlalchemy.ext.asyncio import AsyncSession

from app.model.bookmark import Bookmark
from app.repository.base_repository import BaseRepository


class BookmarkRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[AsyncSession]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Bookmark)
