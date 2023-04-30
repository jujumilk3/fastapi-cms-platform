from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container
from app.core.dependency import get_current_user_token, get_current_user_token_no_exception
from app.model.reaction import ReactionDto
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
    upsert_reaction.user_token = user_token
    return await reaction_service.add(upsert_reaction)


@router.patch("/{reaction_id}", response_model=ReactionDto.WithModelBaseInfo, status_code=status.HTTP_200_OK)
@inject
async def update_reaction(
    reaction_id: int,
    upsert_reaction: ReactionDto.Upsert,
    reaction_service: ReactionService = Depends(Provide[Container.reaction_service]),
    user_token: str = Depends(get_current_user_token),
):
    upsert_reaction.user_token = user_token
    return await reaction_service.patch_after_check_user_token(
        model_id=reaction_id, dto=upsert_reaction, user_token=user_token
    )


@router.delete("/{reaction_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_reaction(
    reaction_id: int,
    reaction_service: ReactionService = Depends(Provide[Container.reaction_service]),
    user_token: str = Depends(get_current_user_token),
):
    await reaction_service.remove_by_id_after_check_user_token(model_id=reaction_id, user_token=user_token)
