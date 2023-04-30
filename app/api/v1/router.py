from fastapi import APIRouter

from app.api.v1.endpoint.admin import router as admin_router
from app.api.v1.endpoint.auth import router as auth_router
from app.api.v1.endpoint.board import router as board_router
from app.api.v1.endpoint.bookmark import router as bookmark_router
from app.api.v1.endpoint.comment import router as comment_router
from app.api.v1.endpoint.debug import router as debug_router
from app.api.v1.endpoint.post import router as post_router
from app.api.v1.endpoint.reaction import router as reaction_router
from app.api.v1.endpoint.tag import router as tag_router
from app.api.v1.endpoint.user import router as user_router

routers = APIRouter()
router_list = [
    admin_router,
    auth_router,
    board_router,
    bookmark_router,
    comment_router,
    debug_router,
    post_router,
    reaction_router,
    tag_router,
    user_router
]

for router in router_list:
    router.tags = routers.tags.append("v1")
    routers.include_router(router)
