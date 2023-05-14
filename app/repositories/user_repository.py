from collections.abc import Callable
from contextlib import AbstractContextManager

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[AsyncSession]]):
        self.session_factory = session_factory
        super().__init__(session_factory, User)

    async def select_user_by_email(self, email: str) -> User:
        async with self.session_factory() as session:
            query = select(User).filter(User.email == email)
            query_result = await session.execute(query)
            found_user = query_result.scalar()
            return found_user

    async def select_user_by_user_token(self, user_token: str) -> User:
        async with self.session_factory() as session:
            query = select(User).filter(User.user_token == user_token)
            query_result = await session.execute(query)
            found_user = query_result.scalar()
            return found_user
