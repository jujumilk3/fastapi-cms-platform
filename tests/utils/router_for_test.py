from fastapi import APIRouter, Body, File, Form, Query, UploadFile
from loguru import logger
from starlette import status

from app.core.exception import CustomHttpException

router = APIRouter()


@router.get("/test_string")
async def get_string():
    return "hello world"


@router.get("/test_dict")
async def get_dict():
    return {"hello": "world"}


@router.get("/test_query")
async def get_query(
    msg: str = Query("hello", description="hello"),
):
    return {"msg": msg}


@router.post("/test_post")
async def post(
    title: str = Body("title", description="title", example="title", embed=True),
    content: str = Body("content", description="content", example="content", embed=True),
):
    return {
        "title": f"response: {title}",
        "content": f"response: {content}",
    }


@router.patch("/test_patch")
async def patch(
    title: str = Body("title", description="title", example="title", embed=True),
    content: str = Body("content", description="content", example="content", embed=True),
):
    return {
        "title": f"response: {title}",
        "content": f"response: {content}",
    }


@router.delete("/test_delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    target_id: int = Query(description="target_id"),
):
    logger.info(f"deleted target_id: {target_id}")


@router.post("/test_post_form")
async def post_form(
    title: str = Form("title", description="title", example="title"),
    content: str = Form("content", description="content", example="content"),
):
    return {
        "title": f"response: {title}",
        "content": f"response: {content}",
    }


@router.post("/complex_case_post")
async def complex_case(
    item_id: int = Query(None, description="item_id", example="item_id"),
    title: str = Body("title", description="title", example="title", embed=True),
    content: str = Body("content", description="content", example="content", embed=True),
):
    return {
        "item_id": item_id,
        "title": f"response: {title}",
        "content": f"response: {content}",
    }


@router.post("/complex_case_form")
async def complex_case_form(
    item_id: int = Query(None, description="item_id", example="item_id"),
    title: str = Form("title", description="title", example="title"),
    content: str = Form("content", description="content", example="content"),
):
    return {
        "item_id": item_id,
        "title": f"response: {title}",
        "content": f"response: {content}",
    }


@router.post("/complex_case_form_and_body")
async def complex_case_form_and_body(
    item_id: int = Query(None, description="item_id", example="item_id"),
    title: str = Form("title", description="title", example="title"),
    content: str = Form("content", description="content", example="content"),
    body: str = Body("body", description="body", example="body", embed=True),
):
    return {
        "item_id": item_id,
        "title": f"response: {title}",
        "content": f"response: {content}",
        "body": f"response: {body}",
    }


@router.post("/test_upload_file")
async def upload_file(
    file: UploadFile = File(None, description="file", example="file"),
):
    return {"file_name": file.filename, "file_content": file.file.read()}


@router.get("/intended_exception")
async def intended_exception():
    raise CustomHttpException(
        status_code=status.HTTP_400_BAD_REQUEST, title="Bad Request", description="This is a detail"
    )
