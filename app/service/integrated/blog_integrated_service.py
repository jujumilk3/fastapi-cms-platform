from app.core.constant import ContentType
from app.model.comment import CommentDto
from app.service import CommentService, PostService, ReactionService, UserService


class BlogIntegratedService:
    def __init__(
        self,
        post_service: PostService,
        comment_service: CommentService,
        reaction_service: ReactionService,
        user_service: UserService,
    ):
        self.post_service = post_service
        self.comment_service = comment_service
        self.reaction_service = reaction_service
        self.user_service = user_service

    async def create_comment_and_update_comment_count(self, upsert_comment: CommentDto.Upsert):
        created_comment = await self.comment_service.add(upsert_comment)
        if created_comment.id and upsert_comment.content_type == ContentType.POST:
            await self.post_service.update_comment_count(created_comment.content_id)
        return created_comment
