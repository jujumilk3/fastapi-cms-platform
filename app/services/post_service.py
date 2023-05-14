from app.repositories.post_repository import PostRepository
from app.services.base_service import BaseService


class PostService(BaseService):
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository
        super().__init__(post_repository)

    async def update_comment_and_reaction_count(self, post_id: int):
        return await self.post_repository.update_comment_and_reaction_count(post_id)

    async def update_comment_count(self, post_id: int):
        return await self.post_repository.update_comment_count(post_id)

    async def update_reaction_count(self, post_id: int):
        return await self.post_repository.update_reaction_count(post_id)
