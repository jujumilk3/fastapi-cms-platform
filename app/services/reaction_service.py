from app.models.reaction import ReactionDto
from app.repositories.reaction_repository import ReactionRepository
from app.services.base_service import BaseService


class ReactionService(BaseService):
    def __init__(self, reaction_repository: ReactionRepository):
        self.reaction_repository = reaction_repository
        super().__init__(reaction_repository)

    async def toggle_reaction(self, upsert_reaction_with_user_token: ReactionDto.UpsertWithUserToken):
        found_reaction = await self.reaction_repository.select_by_content_type_and_content_id_and_user_token(
            **upsert_reaction_with_user_token.dict()
        )
        if found_reaction:
            await self.reaction_repository.delete_by_id(found_reaction.id)
            return
        else:
            return await self.reaction_repository.insert(upsert_reaction_with_user_token)
