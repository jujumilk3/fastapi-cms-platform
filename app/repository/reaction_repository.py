from collections.abc import Callable
from contextlib import AbstractContextManager

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constant import ReactionType
from app.model.reaction import Reaction
from app.repository.base_repository import BaseRepository


class ReactionRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[AsyncSession]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Reaction)

    async def select_by_content_type_and_content_id_and_user_token(
        self, content_type: str, reaction_type: ReactionType, content_id: int, user_token: str
    ) -> Reaction:
        async with self.session_factory() as session:
            query = select(Reaction).filter(
                Reaction.content_type == content_type,
                Reaction.reaction_type == reaction_type,
                Reaction.content_id == content_id,
                Reaction.user_token == user_token,
            )
            query_result = await session.execute(query)
            return query_result.scalar_one_or_none()
