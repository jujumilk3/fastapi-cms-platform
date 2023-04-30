from app.repository.reaction_repository import ReactionRepository
from app.service.base_service import BaseService


class ReactionService(BaseService):
    def __init__(self, reaction_repository: ReactionRepository):
        self.reaction_repository = reaction_repository
        super().__init__(reaction_repository)
