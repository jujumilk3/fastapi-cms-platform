from tests.utils.common import create_bearer_token
from fastapi import status


def test_crud_comment(client, test_name):
    # admin user request
    admin_user_bearer_token = create_bearer_token("admin")
    response = client.post(
        "/v1/admin/board",
        headers={
            "Authorization": admin_user_bearer_token,
        },
        json={
            "display_name": f"test board_{test_name}",
            "manage_name": f"test_board_{test_name}",
            "is_published": True,
            "is_admin_only": False,
            "description": "test board",
            "main_image": "test image",
            "background_image": "test image",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["display_name"] == f"test board_{test_name}"
    assert response.json()["manage_name"] == f"test_board_{test_name}"
    assert response.json()["is_published"] is True
    assert response.json()["is_admin_only"] is False
    assert response.json()["description"] == "test board"
    assert response.json()["main_image"] == "test image"
    assert response.json()["background_image"] == "test image"
    created_board_manage_name = response.json()["manage_name"]

    # normal user request
    normal_user_bearer_token = create_bearer_token("normal")
    response = client.post(
        "/v1/post",
        headers={
            "Authorization": normal_user_bearer_token,
        },
        json={
            "title": f"test post_{test_name}",
            "content": f"test post_{test_name}",
            "language": "ko",
            "is_published": True,
            "is_private": False,
            "board_manage_name": created_board_manage_name,
        },
    )
    created_post_id = response.json()["id"]
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == f"test post_{test_name}"
    assert response.json()["content"] == f"test post_{test_name}"
    assert response.json()["language"] == "ko"
    assert response.json()["is_published"] is True
    assert response.json()["is_private"] is False
    assert response.json()["is_deleted"] is False

    # read
    response = client.get(
        f"/v1/post/{created_post_id}",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == f"test post_{test_name}"
    assert response.json()["content"] == f"test post_{test_name}"
    assert response.json()["language"] == "ko"
    assert response.json()["is_published"] is True
    assert response.json()["is_private"] is False
    assert response.json()["is_deleted"] is False
    assert response.json()["like_count"] == 0
    assert response.json()["comment_count"] == 0

    # other user try to update
    normal_user_bearer_token2 = create_bearer_token("normal2")
    response = client.patch(
        f"/v1/post/{created_post_id}",
        headers={
            "Authorization": normal_user_bearer_token2,
        },
        json={
            "title": f"test post_{test_name}_updated",
            "content": f"test post_{test_name}_updated",
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # author user update
    response = client.patch(
        f"/v1/post/{created_post_id}",
        headers={
            "Authorization": normal_user_bearer_token,
        },
        json={
            "title": f"test post_{test_name}_updated",
            "content": f"test post_{test_name}_updated",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == f"test post_{test_name}_updated"
    assert response.json()["content"] == f"test post_{test_name}_updated"
    assert response.json()["language"] == "ko"
    assert response.json()["is_published"] is True
    assert response.json()["is_private"] is False
    assert response.json()["is_deleted"] is False

    # other user try to delete
    response = client.delete(
        f"/v1/post/{created_post_id}",
        headers={
            "Authorization": normal_user_bearer_token2,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # read after updated
    response = client.get(
        f"/v1/post/{created_post_id}",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == f"test post_{test_name}_updated"
    assert response.json()["content"] == f"test post_{test_name}_updated"
    assert response.json()["language"] == "ko"
    assert response.json()["is_published"] is True
    assert response.json()["is_private"] is False
    assert response.json()["is_deleted"] is False
    assert response.json()["like_count"] == 0
    assert response.json()["comment_count"] == 0

    # write comment without sign in