from tests.utils.common import create_user_and_get_token


def test_crud_reaction(client, test_name):
    # create 15 users and get tokens
    for i in range(15):
        assert "Bearer" in create_user_and_get_token(client, f"test_user_{test_name}_{i}")
