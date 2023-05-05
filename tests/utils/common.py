import json

from app.core.config import config
from app.core.security import create_access_token
from app.model.user import AuthDto


def create_bearer_token(test_user_email: str) -> str:
    access_token = create_access_token(
        AuthDto.Payload(
            email=test_user_email,
            nickname=test_user_email,
            user_token=test_user_email,
        )
    )
    return f"Bearer {access_token['access_token']}"


def read_test_data_from_test_file(file_path: str) -> dict:
    with open(f"{config.TEST_DATA_DIR}/{file_path}") as f:
        return json.loads(f.read())


def create_user_and_get_token(client, user_email: str) -> str:
    user_create_response = client.post(
        "/v1/auth/signup",
        json={
            "email": user_email,
            "password": "1234",
            "nickname": user_email,
        },
    )
    return f"Bearer {user_create_response.json()['access_token']}"
