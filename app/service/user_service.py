from app.model.user import UserDto
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

    async def patch_user_profile_after_check_user_token(self, user_upsert: UserDto.Upsert, user_token: str):
        found_user = await self.user_repository.select_user_by_user_token(user_token)
        if not found_user:
            raise Exception("User not found")
        return await self.patch(found_user.id, user_upsert)
