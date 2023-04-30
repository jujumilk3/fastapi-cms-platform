from app.repository.post_repository import PostRepository
from app.service.base_service import BaseService


class PostService(BaseService):
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository
        super().__init__(post_repository)
