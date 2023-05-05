from tests.utils.common import create_user_and_get_token
from fastapi import status


def test_create_user_and_get_jwt_reaction(client, test_name):
    # create 15 users and get tokens
    for i in range(15):
        assert "Bearer" in create_user_and_get_token(client, f"test_user_{test_name}_{i}")
        # intended fail sign in
        sign_in_response = client.post(
            "/v1/auth/signin",
            json={
                "email": f"test_user_{test_name}_{i}",
                "password": "wrong_password",
            },
        )
        assert sign_in_response.status_code == status.HTTP_401_UNAUTHORIZED

        sign_in_response = client.post(
            "/v1/auth/signin",
            json={
                "email": f"test_user_{test_name}_{i}",
                "password": "1234",
            },
        )
        assert sign_in_response.status_code == status.HTTP_200_OK
