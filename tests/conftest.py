import os

import pytest

from app.core.config import config
from app.main import app

# overwrite ENV and prevent to run pytest from other environments
os.environ["ENV"] = "test"
if os.getenv("ENV") not in ["test"]:
    msg = f"ENV is not test, it is {os.getenv('ENV')}"
    pytest.exit(msg)

import asyncio

import pytest_asyncio
from fastapi.testclient import TestClient
from loguru import logger

from app.model.base_model import Base
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
        # await insert_default_test_data(conn)


@pytest.fixture(scope="session")
def client():
    logger.info(f"config.DB_URL: {config.DB_URL}")
    logger.info("pytest just started")
    logger.info(f"ENV: {os.getenv('ENV')}")
    app.include_router(basic_router_for_test, prefix="/test_only")
    logger.info("client fixture started")
    asyncio.run(create_tables(app.db.engine))
    yield TestClient(app)
