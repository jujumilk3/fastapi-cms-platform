from fastapi import APIRouter

from app.api.v1.endpoint.admin import router as admin_router
from app.api.v1.endpoint.auth import router as auth_router
from app.api.v1.endpoint.board import router as board_router
from app.api.v1.endpoint.debug import router as debug_router
from app.api.v1.endpoint.post import router as post_router
from app.api.v1.endpoint.reaction import router as reaction_router

routers = APIRouter()
router_list = [
    admin_router,
    auth_router,
    board_router,
    debug_router,
    post_router,
    reaction_router,
]

for router in router_list:
    router.tags = routers.tags.append("v1")
    routers.include_router(router)
