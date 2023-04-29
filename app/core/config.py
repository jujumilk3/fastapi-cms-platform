import os
from pathlib import Path

from loguru import logger


class BaseConfig:
    # base
    ENV: str = None
    APP_ROOT_DIR: str = Path(__file__).parent.parent.parent
    TEST_DATA_DIR: str = os.path.join(APP_ROOT_DIR, "tests", "data")
    PROJECT_NAME: str = "techtonic_api"

    # api addresses
    API_PREFIX: str = ""
    API_V1_PREFIX: str = "/v1"
    API_V2_PREFIX: str = "/v2"

    # auth
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_EXPIRE: int = 60 * 60 * 24 * 7  # 7 days
    JWT_REFRESH_EXPIRE: int = 60 * 60 * 24 * 30  # 30 days

    # date
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    # cors
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # database
    DB_URL = "sqlite+aiosqlite:///:memory:"


class TestConfig(BaseConfig):
    # base
    ENV: str = "test"
    DB_URL = "sqlite+aiosqlite:///:memory:"


class DevelopConfig(BaseConfig):
    # base
    ENV: str = "dev"
    DB_URL = "sqlite+aiosqlite:///db.sqlite3"


class StageConfig(BaseConfig):
    # base
    ENV: str = "stage"


class ProductionConfig(BaseConfig):
    # base
    ENV: str = "prod"


ENV = os.getenv("ENV", None)
config = BaseConfig()

if ENV == "test":
    config = TestConfig()
elif ENV == "dev":
    config = DevelopConfig()
elif ENV == "stage":
    config = StageConfig()
elif ENV == "prod":
    config = ProductionConfig()
else:
    logger.info("ENV is not set. It will be set to 'BaseConfig'.")
