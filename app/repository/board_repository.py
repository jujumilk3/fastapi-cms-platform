from collections.abc import Callable
from contextlib import AbstractContextManager

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constant import OrderType
from app.model.board import Board
from app.repository.base_repository import BaseRepository


class BoardRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[AsyncSession]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Board)

    async def select_board_list(
        self,
        offset: int,
        limit: int,
        order: OrderType,
        order_by: str,
        is_published: bool = None,
    ):
        async with self.session_factory() as session:
            where_clauses = []
            if isinstance(is_published, bool):
                where_clauses.append(Board.is_published == is_published)
            query = (
                select(Board)
                .where(*where_clauses)
                .order_by(getattr(getattr(Board, order_by), order)())
                .offset(offset)
                .limit(limit)
            )
            query_result = await session.execute(query)
            return query_result.scalars().all()

    async def select_by_manage_name(self, manage_name: str):
        async with self.session_factory() as session:
            where_clauses = [
                Board.manage_name == manage_name,
            ]
            query = select(Board).where(*where_clauses)
            query_result = await session.execute(query)
            return query_result.scalars().first()
