from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query, status

from app.core.constant import Order
from app.core.container import Container
from app.core.dependency import get_current_user_token_no_exception
from app.model.board import BoardDto
from app.service.board_service import BoardService

router = APIRouter(
    prefix="/board",
    tags=["board"],
    redirect_slashes=False,
)


@router.get("/", response_model=BoardDto.ListResponse, status_code=status.HTTP_200_OK)
@inject
async def get_board_list_by_manage_name(
    offset: int = Query(default=0),
    limit: int = Query(default=20),
    order: Order = Query(default=Order.DESC),
    order_by: str = Query(default="id"),
    board_service: BoardService = Depends(Provide[Container.board_service]),
    user_token: str = Depends(get_current_user_token_no_exception),
):
    result = await board_service.get_board_list(
        offset=offset, limit=limit, order=order, order_by=order_by,
    )
    return BoardDto.ListResponse(
        results=result, offset=offset, limit=limit, total=len(result)
    )
