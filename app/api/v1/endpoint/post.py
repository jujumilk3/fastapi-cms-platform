from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container
from app.core.dependency import get_current_user_token, get_current_user_token_no_exception
from app.model.post import PostDto
from app.service import BoardService
from app.service.post_service import PostService

router = APIRouter(
    prefix="/post",
    tags=["post"],
    redirect_slashes=False,
)


@router.get("/{post_id}", response_model=PostDto.WithModelBaseInfo, status_code=status.HTTP_200_OK)
@inject
async def get_post(
    post_id: int,
    post_service: PostService = Depends(Provide[Container.post_service]),
    user_token: str = Depends(get_current_user_token_no_exception),
):
    return await post_service.get_by_id(post_id)


@router.post("", response_model=PostDto.WithModelBaseInfo, status_code=status.HTTP_201_CREATED)
@inject
async def create_post(
    upsert_post: PostDto.UpsertFeedWithBoardManageName,
    post_service: PostService = Depends(Provide[Container.post_service]),
    board_service: BoardService = Depends(Provide[Container.board_service]),
    user_token: str = Depends(get_current_user_token),
):
    upsert_post.user_token = user_token
    upsert_post.is_deleted = False
    found_board = (
        await board_service.get_by_manage_name(manage_name=upsert_post.board_manage_name)
        if upsert_post.board_manage_name
        else None
    )
    if found_board:
        upsert_post.board_id = found_board.id
    upsert_post.pop("board_manage_name")
    return await post_service.add(upsert_post)


@router.patch("/{post_id}", response_model=PostDto.WithModelBaseInfo, status_code=status.HTTP_200_OK)
@inject
async def update_post(
    post_id: int,
    upsert_post: PostDto.Upsert,
    post_service: PostService = Depends(Provide[Container.post_service]),
    user_token: str = Depends(get_current_user_token),
):
    upsert_post.user_token = user_token
    return await post_service.patch_after_check_user_token(model_id=post_id, dto=upsert_post, user_token=user_token)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_post(
    post_id: int,
    post_service: PostService = Depends(Provide[Container.post_service]),
    user_token: str = Depends(get_current_user_token),
):
    await post_service.remove_by_id_after_check_user_token(model_id=post_id, user_token=user_token)
