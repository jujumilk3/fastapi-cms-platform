import os

import pytest

# overwrite ENV and prevent to run pytest from other environments
os.environ["ENV"] = "test"
if os.getenv("ENV") not in ["test"]:
    msg = f"ENV is not test, it is {os.getenv('ENV')}"
    pytest.exit(msg)

import asyncio
from app.main import app
import pytest_asyncio
from fastapi.testclient import TestClient
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import config

from app.model.base_model import Base
from app.model.user import User
from tests.utils.common import read_test_data_from_test_file
from tests.utils.router_for_test import router as basic_router_for_test


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_name(request):
    return request.node.name


@pytest_asyncio.fixture
async def simple_fixture():
    logger.info("simple_fixture called")
    logger.info(f"simple_fixture id: {(id(simple_fixture))}")
    yield "simple_fixture"


async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await insert_default_test_data(conn)


@pytest.fixture(scope="session")
def client():
    logger.info(f"config.DB_URL: {config.DB_URL}")
    logger.info("pytest just started")
    logger.info(f"ENV: {os.getenv('ENV')}")
    app.include_router(basic_router_for_test, prefix="/test_only")
    logger.info("client fixture started")
    asyncio.run(create_tables(app.db.engine))
    yield TestClient(app)


async def insert_default_test_data(conn):
    logger.info("Just started insert_default_test_data")
    async with AsyncSession(conn) as session:
        super_users = read_test_data_from_test_file("user/super_users.json")
        for super_user in super_users:
            super_user_dict = {}
            for k, v in super_user.items():
                super_user_dict[k] = v
            created_user = User(**super_user_dict)
            session.add(created_user)
            await session.commit()

        normal_users = read_test_data_from_test_file("user/normal_users.json")
        for normal_user in normal_users:
            normal_user_dict = {}
            for k, v in normal_user.items():
                normal_user_dict[k] = v
            created_user = User(**normal_user_dict)
            session.add(created_user)
            await session.commit()

        # check inserted data
        query = select(User).where(User.is_superuser == True)
        query_results = (await session.execute(query)).scalars().all()
        logger.info(f"Created super user: {len(query_results)}")

        query = select(User).where(User.is_superuser == False)
        query_results = (await session.execute(query)).scalars().all()
        logger.info(f"Created normal user: {len(query_results)}")
