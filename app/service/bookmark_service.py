from app.repository.bookmark_repository import BookmarkRepository
from app.service.base_service import BaseService


class BookmarkService(BaseService):
    def __init__(self, bookmark_repository: BookmarkRepository):
        self.bookmark_repository = bookmark_repository
        super().__init__(bookmark_repository)
