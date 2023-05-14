from collections.abc import Callable
from contextlib import AbstractContextManager

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constant import ContentType
from app.models.comment import Comment
from app.repositories.base_repository import BaseRepository


class CommentRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[AsyncSession]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Comment)

    async def select_list_by_post_id(self, post_id: int, offset: int, limit: int):
        async with self.session_factory() as session:
            query = (
                select(Comment)
                .filter(
                    Comment.content_id == post_id,
                    Comment.content_type == ContentType.POST,
            )
            .order_by(Comment.created_at.desc())
            .offset(offset)
            .limit(limit)
            )
            query_result = await session.execute(query)
            return query_result.scalars().all()
