import pytest

from app.core.config import configs


@pytest.mark.order(1)
def test_db_url(db_url):
    assert "sqlite" in configs.DB_URL
    assert "sqlite" in db_url
    assert configs.DB_URL == db_url


def test_test_name_fixture(test_name):
    assert test_name == "test_test_name_fixture"


def test_simple_async_fixture(simple_async_fixture):
    assert simple_async_fixture == "simple_async_fixture"


def test_simple_fixture(simple_fixture):
    assert simple_fixture == "simple_fixture"
