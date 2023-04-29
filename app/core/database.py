from asyncio import current_task

from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine


class Database:
    def __init__(self, db_url: str) -> None:
        # db engine
        self.engine = create_async_engine(db_url)

        # db session factory
        self._session_factory = async_scoped_session(
            session_factory=orm.sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                autocommit=False,
                autoflush=False,
            ),
            scopefunc=current_task,
        )

    @property
    def session_factory(self):
        return self._session_factory
