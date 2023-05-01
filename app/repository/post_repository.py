from collections.abc import Callable
from contextlib import AbstractContextManager

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constant import ContentType
from app.model.post import Post
from app.model.comment import Comment
from app.model.reaction import Reaction
from app.repository.base_repository import BaseRepository


class PostRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[AsyncSession]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Post)

    async def update_comment_and_reaction_count(self, post_id: int):
        async with self.session_factory() as session:
            post = await self.select_by_id(post_id)
            post.comment_count = await session.execute(
                select(Comment).filter(Comment.content_id == post_id, Comment.content_type == ContentType.POST).count()
            )
            post.like_count = await session.execute(
                session.query(Reaction).filter(Reaction.content_id == post_id, Reaction.content_type == ContentType.POST).count()
            )
            await session.merge(post)
            await session.commit()
            return post

    async def update_comment_count(self, post_id: int):
        async with self.session_factory() as session:
            post = await self.select_by_id(post_id)
            post.comment_count = (await session.execute(
                select(func.count(Comment.id)).filter(Comment.content_id == post_id, Comment.content_type == ContentType.POST   )
            )).scalar()
            await session.merge(post)
            await session.commit()
            return post

    async def update_reaction_count(self, post_id: int):
        async with self.session_factory() as session:
            post = await self.select_by_id(post_id)
            post.like_count = await session.execute(
                session.query(Reaction).filter(Reaction.content_id == post_id, Reaction.content_type == ContentType.POST).count()
            )
            await session.merge(post)
            await session.commit()
            return post
