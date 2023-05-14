from asyncio import current_task

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from app.core.config import configs
from app.models.base_model import Base


class Database:
    def __init__(self, db_url: str, sync_db_url: str) -> None:
        # db engine
        self.engine = create_async_engine(db_url)
        self.sync_engine = create_engine(sync_db_url)

        # db session factory
        self._session_factory = async_scoped_session(
            session_factory=sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                autocommit=False,
                autoflush=False,
            ),
            scopefunc=current_task,
        )

        # sync db session factory
        self._sync_session_factory = scoped_session(
            session_factory=sessionmaker(
                bind=self.sync_engine,
                class_=Session,
                autocommit=False,
                autoflush=False,
            ),
            scopefunc=current_task,
        )

        # if run dev, create tables
        if configs.ENV in ["dev"]:
            self.create_tables()

    @property
    def session_factory(self):
        return self._session_factory

    def create_tables(self):
        Base.metadata.create_all(self.sync_engine)
