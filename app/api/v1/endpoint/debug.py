from fastapi import APIRouter, status

from app.core.exception import CustomHttpException

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/exception")
async def get_exception():
    raise CustomHttpException(
        status_code=status.HTTP_400_BAD_REQUEST, title="Bad Request", description="This is a description"
    )
