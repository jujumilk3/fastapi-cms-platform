from fastapi import status

from tests.utils.common import create_bearer_token


def test_crud_post_without_board(client, test_name):
    # not signed-in user request
    response = client.post(
        "/v1/post",
        json={
            "title": f"test post_{test_name}",
            "content": f"test post_{test_name}",
            "language": "ko",
            "is_published": True,
            "is_private": False,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

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

    # author user delete
    response = client.delete(
        f"/v1/post/{created_post_id}",
        headers={
            "Authorization": normal_user_bearer_token,
        },
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # read deleted post
    response = client.get(
        f"/v1/post/{created_post_id}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_crud_post_with_board(client, test_name):
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
    assert response.json()["reaction_count"] == 0
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
    assert response.json()["reaction_count"] == 0
    assert response.json()["comment_count"] == 0

    # author user delete
    response = client.delete(
        f"/v1/post/{created_post_id}",
        headers={
            "Authorization": normal_user_bearer_token,
        },
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # read deleted post
    response = client.get(
        f"/v1/post/{created_post_id}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_comment_count(client, test_name):
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
    assert response.json()["reaction_count"] == 0
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
    assert response.json()["reaction_count"] == 0
    assert response.json()["comment_count"] == 0

    # write comment without sign in
    response = client.post(
        f"/v1/comment",
        json={
            "content_id": created_post_id,
            "content_type": "post",
            "content": "test comment",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # write comment
    response = client.post(
        f"/v1/comment",
        headers={
            "Authorization": normal_user_bearer_token,
        },
        json={
            "content_id": created_post_id,
            "content_type": "post",
            "content": "test comment",
        },
    )
    created_comment_id = response.json()["id"]
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["content_id"] == created_post_id
    assert response.json()["content_type"] == "post"
    assert response.json()["content"] == "test comment"
    assert response.json()["is_deleted"] is False

    # read comment
    response = client.get(
        f"/v1/comment/{created_comment_id}",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["content_id"] == created_post_id
    assert response.json()["content_type"] == "post"
    assert response.json()["content"] == "test comment"
    assert response.json()["is_deleted"] is False

    # check post comment num
    response = client.get(
        f"/v1/post/{created_post_id}",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["comment_count"] == 1

    # update comment without sign in
    response = client.patch(
        f"/v1/comment/{created_comment_id}",
        json={
            "content": "test comment updated",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # update comment with other user
    response = client.patch(
        f"/v1/comment/{created_comment_id}",
        headers={
            "Authorization": normal_user_bearer_token2,
        },
        json={
            "content": "test comment updated",
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # update comment
    response = client.patch(
        f"/v1/comment/{created_comment_id}",
        headers={
            "Authorization": normal_user_bearer_token,
        },
        json={
            "content": "test comment updated",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["content_id"] == created_post_id
    assert response.json()["content_type"] == "post"
    assert response.json()["content"] == "test comment updated"
    assert response.json()["is_deleted"] is False

    # delete comment without sign in
    response = client.delete(
        f"/v1/comment/{created_comment_id}",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # delete comment with other user
    response = client.delete(
        f"/v1/comment/{created_comment_id}",
        headers={
            "Authorization": normal_user_bearer_token2,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # delete comment
    response = client.delete(
        f"/v1/comment/{created_comment_id}",
        headers={
            "Authorization": normal_user_bearer_token,
        },
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
