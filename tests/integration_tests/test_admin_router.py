from fastapi import status

from tests.utils.common import create_bearer_token


def test_check_admin(client, test_name):
    # request without token
    response = client.get(
        "/v1/admin/iam",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # normal user request
    normal_user_bearer_token = create_bearer_token("normal")
    response = client.get(
        "/v1/admin/iam",
        headers={
            "Authorization": normal_user_bearer_token,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "It's not a super user"

    # admin user request
    super_user_bearer_token = create_bearer_token("admin")
    response = client.get(
        "/v1/admin/iam",
        headers={
            "Authorization": super_user_bearer_token,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] is True


def test_crud_board(client, test_name):
    response = client.post(
        "/v1/admin/board",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # normal user request
    normal_user_bearer_token = create_bearer_token("normal")
    response = client.post(
        "/v1/admin/board",
        headers={
            "Authorization": normal_user_bearer_token,
        },
        json={
            "display_name": f"test board_{test_name}",
            "manage_name": f"test_board_{test_name}",
            "is_published": True,
            "is_admin_only": False,
            "description": "test board",
            "main_image": "test image",
            "background_image": "test image",
        }
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

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
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["display_name"] == f"test board_{test_name}"
    assert response.json()["manage_name"] == f"test_board_{test_name}"
    assert response.json()["is_published"] is True
    assert response.json()["is_admin_only"] is False
    assert response.json()["description"] == "test board"
    assert response.json()["main_image"] == "test image"
    assert response.json()["background_image"] == "test image"

    # read
    board_id = response.json()["id"]
    response = client.get(
        f"/v1/admin/board/{board_id}",
        headers={
            "Authorization": admin_user_bearer_token,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["display_name"] == f"test board_{test_name}"
    assert response.json()["manage_name"] == f"test_board_{test_name}"
    assert response.json()["is_published"] is True
    assert response.json()["is_admin_only"] is False
    assert response.json()["description"] == "test board"
    assert response.json()["main_image"] == "test image"
    assert response.json()["background_image"] == "test image"

    # update
    response = client.patch(
        f"/v1/admin/board/{board_id}",
        headers={
            "Authorization": admin_user_bearer_token,
        },
        json={
            "display_name": f"test board_{test_name}_updated",
            "manage_name": f"test_board_{test_name}_updated",
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["display_name"] == f"test board_{test_name}_updated"
    assert response.json()["manage_name"] == f"test_board_{test_name}_updated"
    assert response.json()["is_published"] is True
    assert response.json()["is_admin_only"] is False
    assert response.json()["description"] == "test board"
    assert response.json()["main_image"] == "test image"
    assert response.json()["background_image"] == "test image"

    # read after update
    response = client.get(
        f"/v1/admin/board/{board_id}",
        headers={
            "Authorization": admin_user_bearer_token,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["display_name"] == f"test board_{test_name}_updated"
    assert response.json()["manage_name"] == f"test_board_{test_name}_updated"
    assert response.json()["is_published"] is True
    assert response.json()["is_admin_only"] is False
    assert response.json()["description"] == "test board"
    assert response.json()["main_image"] == "test image"
    assert response.json()["background_image"] == "test image"

    # delete
    response = client.delete(
        f"/v1/admin/board/{board_id}",
        headers={
            "Authorization": admin_user_bearer_token,
        },
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # read after delete
    response = client.get(
        f"/v1/admin/board/{board_id}",
        headers={
            "Authorization": admin_user_bearer_token,
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
