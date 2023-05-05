from fastapi import status

from app.core.constant import ContentType, ReactionType
from tests.utils.common import create_bearer_token


def test_crud_reaction(client, test_name):
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

    # normal user request to create post
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

    # normal user request to create reaction
    response = client.post(
        "/v1/reaction",
        headers={
            "Authorization": normal_user_bearer_token,
        },
        json={
            "content_id": created_post_id,
            "content_type": ContentType.POST,
            "reaction_type": ReactionType.LIKE,
        },
    )
    created_reaction_id = response.json()["id"]
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["content_id"] == created_post_id
    assert response.json()["content_type"] == ContentType.POST
    assert response.json()["reaction_type"] == ReactionType.LIKE

    # get created reaction
    response = client.get(
        f"v1/reaction/{created_reaction_id}",
        headers={
            "Authorization": normal_user_bearer_token,
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == created_reaction_id
    assert response.json()["content_id"] == created_post_id
    assert response.json()["content_type"] == ContentType.POST
    assert response.json()["reaction_type"] == ReactionType.LIKE

    # delete created reaction
    response = client.delete(
        f"v1/reaction/{created_reaction_id}",
        headers={
            "Authorization": normal_user_bearer_token,
        }
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # toggle reaction
    response = client.post(
        "/v1/reaction/toggle",
        headers={
            "Authorization": normal_user_bearer_token,
        },
        json={
            "content_id": created_post_id,
            "content_type": ContentType.POST,
            "reaction_type": ReactionType.LIKE,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["content_id"] == created_post_id
    assert response.json()["content_type"] == ContentType.POST
    assert response.json()["reaction_type"] == ReactionType.LIKE

    response = client.post(
        "/v1/reaction/toggle",
        headers={
            "Authorization": normal_user_bearer_token,
        },
        json={
            "content_id": created_post_id,
            "content_type": ContentType.POST,
            "reaction_type": ReactionType.LIKE,
        },
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
