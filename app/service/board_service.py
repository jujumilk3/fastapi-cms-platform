from app.core.constant import Order
from app.repository.board_repository import BoardRepository
from app.service.base_service import BaseService


class BoardService(BaseService):
    def __init__(self, board_repository: BoardRepository):
        self.board_repository = board_repository
        super().__init__(board_repository)

    async def get_board_list(self, offset: int, limit: int, order: Order, order_by: str):
        return await self.board_repository.select_board_list(
            offset=offset,
            limit=limit,
            order=order,
            order_by=order_by,
        )

    async def get_by_manage_name(self, manage_name: str):
        return await self.board_repository.select_by_manage_name(manage_name)
