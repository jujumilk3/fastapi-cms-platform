from app.repositories.comment_repository import CommentRepository
from app.services.base_service import BaseService


class CommentService(BaseService):
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository
        super().__init__(comment_repository)

    async def get_list_by_post_id(self, post_id: int, offset: int, limit: int):
        return await self.comment_repository.select_list_by_post_id(post_id=post_id, offset=offset, limit=limit)
