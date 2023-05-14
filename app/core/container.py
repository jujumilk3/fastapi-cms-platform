from dependency_injector import containers, providers

from app import repository, service
from app.core.config import configs
from app.core.database import Database


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.endpoint.admin",
            "app.api.v1.endpoint.auth",
            "app.api.v1.endpoint.board",
            "app.api.v1.endpoint.bookmark",
            "app.api.v1.endpoint.comment",
            "app.api.v1.endpoint.debug",
            "app.api.v1.endpoint.post",
            "app.api.v1.endpoint.reaction",
            "app.api.v1.endpoint.tag",
            "app.api.v1.endpoint.user",
        ]
    )
    db = providers.Singleton(Database, db_url=configs.DB_URL, sync_db_url=configs.SYNC_DB_URL)

    # Base repositories
    board_repository = providers.Factory(repository.BoardRepository, session_factory=db.provided.session_factory)
    bookmark_repository = providers.Factory(repository.BookmarkRepository, session_factory=db.provided.session_factory)
    comment_repository = providers.Factory(repository.CommentRepository, session_factory=db.provided.session_factory)
    post_repository = providers.Factory(repository.PostRepository, session_factory=db.provided.session_factory)
    reaction_repository = providers.Factory(repository.ReactionRepository, session_factory=db.provided.session_factory)
    tag_repository = providers.Factory(repository.TagRepository, session_factory=db.provided.session_factory)
    user_repository = providers.Factory(repository.UserRepository, session_factory=db.provided.session_factory)

    # Base services
    auth_service = providers.Factory(service.AuthService, user_repository=user_repository)
    board_service = providers.Factory(service.BoardService, board_repository=board_repository)
    bookmark_service = providers.Factory(service.BookmarkService, bookmark_repository=bookmark_repository)
    comment_service = providers.Factory(service.CommentService, comment_repository=comment_repository)
    post_service = providers.Factory(service.PostService, post_repository=post_repository)
    reaction_service = providers.Factory(service.ReactionService, reaction_repository=reaction_repository)
    tag_service = providers.Factory(service.TagService, tag_repository=tag_repository)
    user_service = providers.Factory(service.UserService, user_repository=user_repository)

    # Integrated services
    cms_integrated_service = providers.Factory(
        service.CmsIntegratedService,
        post_service=post_service,
        comment_service=comment_service,
        reaction_service=reaction_service,
        user_service=user_service,
    )
