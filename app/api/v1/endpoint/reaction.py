from typing import Union, Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status, Response

from app.core.constant import ContentType
from app.core.container import Container
from app.core.dependency import get_current_user_token, get_current_user_token_no_exception
from app.model.reaction import ReactionDto
from app.service import PostService
from app.service.reaction_service import ReactionService

router = APIRouter(
    prefix="/reaction",
    tags=["reaction"],
    redirect_slashes=False,
)


@router.get("/{reaction_id}", response_model=ReactionDto.WithModelBaseInfo, status_code=status.HTTP_200_OK)
@inject
async def get_reaction(
    reaction_id: int,
    reaction_service: ReactionService = Depends(Provide[Container.reaction_service]),
    user_token: str = Depends(get_current_user_token_no_exception),
):
    return await reaction_service.get_by_id(reaction_id)


@router.post("", response_model=ReactionDto.WithModelBaseInfo, status_code=status.HTTP_201_CREATED)
@inject
async def create_reaction(
    upsert_reaction: ReactionDto.Upsert,
    reaction_service: ReactionService = Depends(Provide[Container.reaction_service]),
    user_token: str = Depends(get_current_user_token),
):
    upsert_reaction_with_user_token = ReactionDto.UpsertWithUserToken(**upsert_reaction.dict(), user_token=user_token)
    return await reaction_service.add(upsert_reaction_with_user_token)


@router.delete("/{reaction_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_reaction(
    reaction_id: int,
    reaction_service: ReactionService = Depends(Provide[Container.reaction_service]),
    user_token: str = Depends(get_current_user_token),
):
    await reaction_service.remove_by_id_after_check_user_token(model_id=reaction_id, user_token=user_token)


@router.post("/toggle", response_model=Union[ReactionDto.WithModelBaseInfo, Any])
@inject
async def toggle_reaction(
    response: Response,
    upsert_reaction: ReactionDto.Upsert,
    reaction_service: ReactionService = Depends(Provide[Container.reaction_service]),
    post_service: PostService = Depends(Provide[Container.post_service]),
    user_token: str = Depends(get_current_user_token),
):
    upsert_reaction_with_user_token = ReactionDto.UpsertWithUserToken(**upsert_reaction.dict(), user_token=user_token)
    result = await reaction_service.toggle_reaction(upsert_reaction_with_user_token=upsert_reaction_with_user_token)
    response.status_code = status.HTTP_201_CREATED if result else status.HTTP_204_NO_CONTENT
    if upsert_reaction.content_type == ContentType.POST:
        await post_service.update_reaction_count(upsert_reaction.content_id)
    return result
