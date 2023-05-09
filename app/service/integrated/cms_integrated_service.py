from app.core.constant import ContentType
from app.model.comment import Comment, CommentDto
from app.service import CommentService, PostService, ReactionService, UserService


class CmsIntegratedService:
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

    async def remove_comment_after_check_user_token_and_update_comment_count(self, comment_id: int, user_token: str):
        found_comment: Comment = await self.comment_service.get_by_id(comment_id)
        await self.comment_service.remove_by_id_after_check_user_token(model_id=comment_id, user_token=user_token)
        if found_comment.content_type == ContentType.POST:
            await self.post_service.update_comment_count(found_comment.content_id)

    async def create_reaction_and_update_reaction_count(self, upsert_reaction: CommentDto.Upsert):
        created_reaction = await self.reaction_service.add(upsert_reaction)
        if created_reaction.id and upsert_reaction.content_type == ContentType.POST:
            await self.post_service.update_reaction_count(created_reaction.content_id)
        return created_reaction

    async def remove_reaction_after_check_user_token_and_update_reaction_count(self, reaction_id: int, user_token: str):
        found_reaction: Comment = await self.reaction_service.get_by_id(reaction_id)
        await self.reaction_service.remove_by_id_after_check_user_token(model_id=reaction_id, user_token=user_token)
        if found_reaction.content_type == ContentType.POST:
            await self.post_service.update_reaction_count(found_reaction.content_id)
