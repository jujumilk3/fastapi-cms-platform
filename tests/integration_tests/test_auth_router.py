from fastapi import status

from app.model.user import AuthDto


def test_sign_up_and_sign_in(client):
    sign_up_info = {"email": "test@test.com", "password": "test", "nickname": "test"}
    sign_up_response = client.post("/v1/auth/signup", json=sign_up_info)
    assert sign_up_response.status_code == status.HTTP_201_CREATED
    assert AuthDto.JWTPayload(**sign_up_response.json())
    assert sign_up_response.json()["access_token"]
    assert sign_up_response.json()["expiration"]
    assert sign_up_response.json()["email"] == sign_up_info["email"]
    assert sign_up_response.json()["nickname"] == sign_up_info["nickname"]
    assert sign_up_response.json()["user_token"]

    sign_in_info = {"email": "test@test.com", "password": "test"}
    sign_in_response = client.post("/v1/auth/signin", json=sign_in_info)
    assert sign_in_response.status_code == status.HTTP_200_OK
    assert AuthDto.JWTPayload(**sign_in_response.json())
    assert sign_in_response.json()["access_token"]
    assert sign_in_response.json()["expiration"]
    assert sign_in_response.json()["email"] == sign_up_info["email"]
    assert sign_in_response.json()["nickname"] == sign_up_info["nickname"]
    assert sign_in_response.json()["user_token"]

    get_me_response = client.get(
        "/v1/auth/me", headers={"Authorization": f"Bearer {sign_in_response.json()['access_token']}"}
    )
    assert get_me_response.status_code == status.HTTP_200_OK
    assert get_me_response.json()["email"] == sign_up_info["email"]
    assert get_me_response.json()["nickname"] == sign_up_info["nickname"]
    assert get_me_response.json()["user_token"] == sign_in_response.json()["user_token"]
