from pydantic import BaseModel


class BaseService:
    def __init__(self, repository) -> None:
        self._repository = repository

    async def get_by_id(self, model_id: int):
        return await self._repository.select_by_id(model_id=model_id)

    async def get_by_id_after_check_is_deleted(self, model_id: int):
        return await self._repository.select_by_id_after_check_is_deleted(model_id=model_id)

    async def get_by_ids(self, model_ids: list[int]):
        return await self._repository.select_by_ids(model_ids=model_ids)

    async def add(self, dto: BaseModel):
        return await self._repository.insert(dto=dto)

    async def patch(self, model_id: int, dto: BaseModel):
        return await self._repository.update(model_id=model_id, dto=dto)

    async def upsert(self, model_id: int, dto: BaseModel):
        return await self._repository.upsert(model_id=model_id, dto=dto)

    async def patch_after_check_user_token(self, model_id: int, dto: BaseModel, user_token: str):
        return await self._repository.update_after_check_user_token(model_id=model_id, dto=dto, user_token=user_token)

    async def remove_by_id(self, model_id: int):
        return await self._repository.delete_by_id(model_id=model_id)

    async def remove_by_id_after_check_user_token(self, model_id: int, user_token: str):
        return await self._repository.delete_by_id_after_check_user_token(model_id=model_id, user_token=user_token)

    async def soft_remove_by_id_after_check_user_token(self, model_id: int, user_token: str):
        return await self._repository.soft_delete_by_id_after_check_user_token(model_id=model_id, user_token=user_token)

    async def toggle_with_user_token(self, model_id: int, user_token: str):
        found_model = await self.get_by_id(model_id=model_id)
        if found_model.user_token == user_token:
            return await self.remove_by_id(model_id=model_id)
        else:
            return await self.add(dto=found_model)
