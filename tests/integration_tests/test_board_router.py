from tests.utils.common import create_bearer_token
from fastapi import status
import time


def test_board_list_with_params(client, test_name):
    admin_user_bearer_token = create_bearer_token("admin")
    # create 30 boards
    for i in range(30):
        response = client.post(
            "/v1/admin/board",
            headers={
                "Authorization": admin_user_bearer_token,
            },
            json={
                "display_name": f"test board{test_name}_{i}",
                "manage_name": f"test_board{test_name}_{i}",
                "is_published": True,
                "is_admin_only": False,
                "description": "test board",
                "main_image": "test image",
                "background_image": "test image",
            }
        )
        assert response.status_code == status.HTTP_201_CREATED

    # get list
    response = client.get(
        "/v1/board",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["offset"] == 0
    assert response.json()["limit"] == 20
    assert response.json()["total"] == 20

    # get list 10
    response = client.get(
        "/v1/board",
        params={
            "limit": 10,
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["offset"] == 0
    assert response.json()["limit"] == 10
    assert response.json()["total"] == 10

    # get list 10 with offset 10
    response = client.get(
        "/v1/board",
        params={
            "limit": 10,
            "offset": 10,
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["offset"] == 10
    assert response.json()["limit"] == 10
    assert response.json()["total"] == 10
    assert response.json()["results"][0]["display_name"] == f"test board{test_name}_19"


def test_board_list_with_order(client):
    admin_user_bearer_token = create_bearer_token("admin")
    # create 5 boards
    for i in range(5):
        response = client.post(
            "/v1/admin/board",
            headers={
                "Authorization": admin_user_bearer_token,
            },
            json={
                "display_name": f"test board_{i}",
                "manage_name": f"test_board_{i}",
                "is_published": True,
                "is_admin_only": False,
                "description": "test board",
                "main_image": "test image",
                "background_image": "test image",
            }
        )
        time.sleep(1)
        assert response.status_code == status.HTTP_201_CREATED

    # get list
    response = client.get(
        "/v1/board",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["offset"] == 0
    assert response.json()["limit"] == 20
    assert response.json()["total"] == 5

    # check order with default order_by=id desc
    for i in range(5):
        assert response.json()["results"][i]["display_name"] == f"test board_{4 - i}"

    # get list with order_by=created_at asc
    response = client.get(
        "/v1/board",
        params={
            "order_by": "created_at",
            "order": "asc",
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["offset"] == 0
    assert response.json()["limit"] == 20

    # check order with order_by=created_at asc
    for i in range(5):
        assert response.json()["results"][i]["display_name"] == f"test board_{i}"
