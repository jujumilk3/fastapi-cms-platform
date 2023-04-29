from app.repository.user_repository import UserRepository
from app.service.base_service import BaseService


class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    async def get_user_by_email(self, email: str):
        return await self.user_repository.select_user_by_email(email)

    async def get_user_by_user_token(self, user_token: str):
        return await self.user_repository.select_user_by_user_token(user_token)
