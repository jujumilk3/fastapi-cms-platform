from app.repositories.comment_repository import CommentRepository
from app.services.base_service import BaseService


class CommentService(BaseService):
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository
        super().__init__(comment_repository)
