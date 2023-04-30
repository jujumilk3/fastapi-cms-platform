import time

from fastapi import status

from tests.utils.common import create_bearer_token


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
            },
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
        },
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
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["offset"] == 10
    assert response.json()["limit"] == 10
    assert response.json()["total"] == 10
    assert response.json()["results"][0]["display_name"] == f"test board{test_name}_19"

    # get id desc
    response = client.get(
        "/v1/board",
        params={
            "offset": 0,
            "limit": 30,
        }
    )
    assert response.status_code == status.HTTP_200_OK
    for i in range(30):
        assert response.json()["results"][i]["display_name"] == f"test board{test_name}_{29 - i}"

    # get id asc
    response = client.get(
        "/v1/board",
        params={
            "offset": 0,
            "limit": 30,
            "order_by": "id",
            "order": "asc",
        }
    )
    assert response.status_code == status.HTTP_200_OK
    for i in range(30):
        assert response.json()["results"][i]["display_name"] == f"test board{test_name}_{i}"
