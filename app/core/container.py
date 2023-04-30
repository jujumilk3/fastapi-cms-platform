from dependency_injector import containers, providers

from app import repository, service
from app.core.config import config
from app.core.database import Database


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.endpoint.admin",
            "app.api.v1.endpoint.auth",
            "app.api.v1.endpoint.board",
            "app.api.v1.endpoint.debug",
            "app.api.v1.endpoint.post",
        ]
    )
    db = providers.Singleton(Database, db_url=config.DB_URL)

    # Base repositories
    board_repository = providers.Factory(repository.BoardRepository, session_factory=db.provided.session_factory)
    user_repository = providers.Factory(repository.UserRepository, session_factory=db.provided.session_factory)
    post_repository = providers.Factory(repository.PostRepository, session_factory=db.provided.session_factory)

    # Base services
    auth_service = providers.Factory(service.AuthService, user_repository=user_repository)
    board_service = providers.Factory(service.BoardService, board_repository=board_repository)
    user_service = providers.Factory(service.UserService, user_repository=user_repository)
    post_service = providers.Factory(service.PostService, post_repository=post_repository)

    # Integrated services
