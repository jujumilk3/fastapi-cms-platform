from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container
from app.core.dependency import get_current_user_token, get_current_user_token_no_exception
from app.models.comment import CommentDto
from app.services.comment_service import CommentService
from app.services.integrated.cms_integrated_service import CmsIntegratedService

router = APIRouter(
    prefix="/comment",
    tags=["comment"],
    redirect_slashes=False,
)


@router.get("/{comment_id}", response_model=CommentDto.WithModelBaseInfo, status_code=status.HTTP_200_OK)
@inject
async def get_comment(
    comment_id: int,
    comment_service: CommentService = Depends(Provide[Container.comment_service]),
    user_token: str = Depends(get_current_user_token_no_exception),
):
    return await comment_service.get_by_id(comment_id)


@router.post("", response_model=CommentDto.WithModelBaseInfo, status_code=status.HTTP_201_CREATED)
@inject
async def create_comment(
    upsert_comment: CommentDto.Upsert,
    cms_integrated_service: CmsIntegratedService = Depends(Provide[Container.cms_integrated_service]),
    user_token: str = Depends(get_current_user_token),
):
    upsert_comment_with_user_token = CommentDto.UpsertWithUserToken(**upsert_comment.dict(), user_token=user_token)
    return await cms_integrated_service.create_comment_and_update_comment_count(upsert_comment_with_user_token)


@router.patch("/{comment_id}", response_model=CommentDto.WithModelBaseInfo, status_code=status.HTTP_200_OK)
@inject
async def update_comment(
    comment_id: int,
    upsert_comment: CommentDto.Upsert,
    comment_service: CommentService = Depends(Provide[Container.comment_service]),
    user_token: str = Depends(get_current_user_token),
):
    upsert_comment_with_user_token = CommentDto.UpsertWithUserToken(**upsert_comment.dict(), user_token=user_token)
    return await comment_service.patch_after_check_user_token(
        model_id=comment_id, dto=upsert_comment_with_user_token, user_token=user_token
    )


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_comment(
    comment_id: int,
    cms_integrated_service: CmsIntegratedService = Depends(Provide[Container.cms_integrated_service]),
    user_token: str = Depends(get_current_user_token),
):
    await cms_integrated_service.remove_comment_after_check_user_token_and_update_comment_count(
        comment_id=comment_id, user_token=user_token
    )
