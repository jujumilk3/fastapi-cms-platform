from dependency_injector import containers, providers

from app import repositories, services
from app.core.config import configs
from app.core.database import Database


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.endpoints.admin",
            "app.api.v1.endpoints.auth",
            "app.api.v1.endpoints.board",
            "app.api.v1.endpoints.bookmark",
            "app.api.v1.endpoints.comment",
            "app.api.v1.endpoints.debug",
            "app.api.v1.endpoints.post",
            "app.api.v1.endpoints.reaction",
            "app.api.v1.endpoints.tag",
            "app.api.v1.endpoints.user",
        ]
    )
    db = providers.Singleton(Database, db_url=configs.DB_URL, sync_db_url=configs.SYNC_DB_URL)

    # Base repositories
    board_repository = providers.Factory(repositories.BoardRepository, session_factory=db.provided.session_factory)
    bookmark_repository = providers.Factory(repositories.BookmarkRepository, session_factory=db.provided.session_factory)
    comment_repository = providers.Factory(repositories.CommentRepository, session_factory=db.provided.session_factory)
    post_repository = providers.Factory(repositories.PostRepository, session_factory=db.provided.session_factory)
    reaction_repository = providers.Factory(repositories.ReactionRepository, session_factory=db.provided.session_factory)
    tag_repository = providers.Factory(repositories.TagRepository, session_factory=db.provided.session_factory)
    user_repository = providers.Factory(repositories.UserRepository, session_factory=db.provided.session_factory)

    # Base services
    auth_service = providers.Factory(services.AuthService, user_repository=user_repository)
    board_service = providers.Factory(services.BoardService, board_repository=board_repository)
    bookmark_service = providers.Factory(services.BookmarkService, bookmark_repository=bookmark_repository)
    comment_service = providers.Factory(services.CommentService, comment_repository=comment_repository)
    post_service = providers.Factory(services.PostService, post_repository=post_repository)
    reaction_service = providers.Factory(services.ReactionService, reaction_repository=reaction_repository)
    tag_service = providers.Factory(services.TagService, tag_repository=tag_repository)
    user_service = providers.Factory(services.UserService, user_repository=user_repository)

    # Integrated services
    cms_integrated_service = providers.Factory(
        services.CmsIntegratedService,
        post_service=post_service,
        comment_service=comment_service,
        reaction_service=reaction_service,
        user_service=user_service,
    )
