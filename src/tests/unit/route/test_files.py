from fastapi.testclient import TestClient
import main
import os

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
                "/upload/",
                files={"file": (test_file_name, file, "text/plain")}
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
                "/upload/",
                files={"file": (test_file_name, file, "text/plain")}
            )

        response = client.get(f"/download/{test_file_name}")
        assert response.status_code == 200
        assert response.content == test_file_content
    finally:
        remove_test_file()
