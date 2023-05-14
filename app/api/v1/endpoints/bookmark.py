from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container
from app.core.dependency import get_current_user_token, get_current_user_token_no_exception
from app.models.bookmark import BookmarkDto
from app.services.bookmark_service import BookmarkService

router = APIRouter(
    prefix="/bookmark",
    tags=["bookmark"],
    redirect_slashes=False,
)


@router.get("/{bookmark_id}", response_model=BookmarkDto.WithModelBaseInfo, status_code=status.HTTP_200_OK)
@inject
async def get_bookmark(
    bookmark_id: int,
    bookmark_service: BookmarkService = Depends(Provide[Container.bookmark_service]),
    user_token: str = Depends(get_current_user_token_no_exception),
):
    return await bookmark_service.get_by_id(bookmark_id)


@router.post("", response_model=BookmarkDto.WithModelBaseInfo, status_code=status.HTTP_201_CREATED)
@inject
async def create_bookmark(
    upsert_bookmark: BookmarkDto.Upsert,
    bookmark_service: BookmarkService = Depends(Provide[Container.bookmark_service]),
    user_token: str = Depends(get_current_user_token),
):
    upsert_bookmark.user_token = user_token
    return await bookmark_service.add(upsert_bookmark)


@router.patch("/{bookmark_id}", response_model=BookmarkDto.WithModelBaseInfo, status_code=status.HTTP_200_OK)
@inject
async def update_bookmark(
    bookmark_id: int,
    upsert_bookmark: BookmarkDto.Upsert,
    bookmark_service: BookmarkService = Depends(Provide[Container.bookmark_service]),
    user_token: str = Depends(get_current_user_token),
):
    upsert_bookmark.user_token = user_token
    return await bookmark_service.patch_after_check_user_token(
        model_id=bookmark_id, dto=upsert_bookmark, user_token=user_token
    )


@router.delete("/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_bookmark(
    bookmark_id: int,
    bookmark_service: BookmarkService = Depends(Provide[Container.bookmark_service]),
    user_token: str = Depends(get_current_user_token),
):
    await bookmark_service.remove_by_id_after_check_user_token(model_id=bookmark_id, user_token=user_token)
