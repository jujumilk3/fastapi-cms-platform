from collections.abc import Callable
from contextlib import AbstractContextManager

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constant import ContentType
from app.models.comment import Comment
from app.models.post import Post
from app.models.reaction import Reaction
from app.repositories.base_repository import BaseRepository


class PostRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[AsyncSession]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Post)

    async def update_comment_and_reaction_count(self, post_id: int):
        async with self.session_factory() as session:
            post = await self.select_by_id(post_id)
            post.comment_count = await session.execute(
                select(Comment)
                .filter(
                    Comment.content_id == post_id,
                    Comment.content_type == ContentType.POST,
                )
                .count()
            )
            post.like_count = await session.execute(
                session.query(Reaction)
                .filter(
                    Reaction.content_id == post_id,
                    Reaction.content_type == ContentType.POST,
                )
                .count()
            )
            await session.merge(post)
            await session.commit()
            return post

    async def update_comment_count(self, post_id: int):
        async with self.session_factory() as session:
            post = await self.select_by_id(post_id)
            query = select(func.count(Comment.id)).filter(
                Comment.content_id == post_id,
                Comment.content_type == ContentType.POST,
            )
            query_result = await session.execute(query)
            post.comment_count = query_result.scalar_one_or_none() or 0
            await session.merge(post)
            await session.commit()
            return post

    async def update_reaction_count(self, post_id: int):
        async with self.session_factory() as session:
            post = await self.select_by_id(post_id)
            query = select(func.count(Reaction.id)).filter(
                Reaction.content_id == post_id,
                Reaction.content_type == ContentType.POST,
            )
            query_result = await session.execute(query)
            post.reaction_count = query_result.scalar_one_or_none() or 0
            await session.merge(post)
            await session.commit()
            return post
