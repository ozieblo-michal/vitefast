import os

from fastapi.testclient import TestClient

import main

client = TestClient(main.app)

test_file_name = "test_file.txt"
test_file_content = b"test content"


def create_test_file():
    with open(test_file_name, "wb") as file:
        file.write(test_file_content)


def remove_test_file():
    if os.path.exists(test_file_name):
        os.remove(test_file_name)


def test_upload_file():
    create_test_file()
    try:
        with open(test_file_name, "rb") as file:
            response = client.post(
                "/upload/", files={"file": (test_file_name, file, "text/plain")}
            )
        assert response.status_code == 200
        assert response.json().get("filename") == test_file_name
    finally:
        remove_test_file()


def test_download_file():
    create_test_file()
    try:
        with open(test_file_name, "rb") as file:
            client.post(
                "/upload/", files={"file": (test_file_name, file, "text/plain")}
            )

        response = client.get(f"/download/{test_file_name}")
        assert response.status_code == 200
        assert response.content == test_file_content
    finally:
        remove_test_file()


import httpx
import pytest

app = main.app

@pytest.mark.asyncio
async def test_upload_file_type():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:

        response = await client.post(
            "/upload",
            files={"file": ("test.csv", "dummy content", "text/csv")}
        )
        assert response.status_code == 200


        response = await client.post(
            "/upload",
            files={"file": ("test.exe", "dummy content", "application/octet-stream")}
        )
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_upload_file_size():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:

        small_file_content = b"a" * (2*1024*1024 - 1)  
        
        response = await client.post(
            "/upload",
            files={"file": ("small_file.txt", small_file_content)}
        )
        assert response.status_code == 200


        large_file_content = b"a" * (2*1024*1024 + 1)  
        
        response = await client.post(
            "/upload",
            files={"file": ("large_file.txt", large_file_content)}
        )
        assert response.status_code == 413


