import os
import main
import httpx
import pytest
import boto3

from fastapi.testclient import TestClient
from moto import mock_s3, mock_ec2


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


app = main.app


@pytest.mark.asyncio
async def test_upload_file_type():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/upload", files={"file": ("test.csv", "dummy content", "text/csv")}
        )
        assert response.status_code == 200

        response = await client.post(
            "/upload",
            files={"file": ("test.exe", "dummy content", "application/octet-stream")},
        )
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_upload_file_size():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        small_file_content = b"a" * (2 * 1024 * 1024 - 1)

        response = await client.post(
            "/upload", files={"file": ("small_file.txt", small_file_content)}
        )
        assert response.status_code == 200

        large_file_content = b"a" * (2 * 1024 * 1024 + 1)

        response = await client.post(
            "/upload", files={"file": ("large_file.txt", large_file_content)}
        )
        assert response.status_code == 413


@mock_ec2
def test_my_ec2():
    ec2 = boto3.resource("ec2", region_name="us-east-1")
    ec2.create_instances(ImageId="ami-1234abcd", MinCount=1, MaxCount=1)

    instances = list(ec2.instances.all())
    for instance in instances:
        print(instance.id, instance.state)


@pytest.fixture(scope="function")
def s3_mock():
    with mock_s3():
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="test-bucket")
        yield s3


@pytest.fixture(scope="function")
def test_app(s3_mock):
    os.environ["S3_BUCKET_NAME"] = "test-bucket"
    client = TestClient(app)
    yield client


def test_upload_to_s3_moto(test_app, s3_mock):
    response = test_app.post(
        "/uploads3/", files={"file": ("testfile.txt", b"test content", "text/plain")}
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "The file has been successfully uploaded to S3"
    }

    objects_in_bucket = s3_mock.list_objects(Bucket="test-bucket")
    filenames = [obj["Key"] for obj in objects_in_bucket.get("Contents", [])]
    assert "folder/testfile.txt" in filenames


def test_delete_local_file():
    test_file_name = "test_file_to_delete.txt"
    test_file_content = b"test content"

    upload_folder = "uploads"

    os.makedirs(upload_folder, exist_ok=True)
    test_file_path = os.path.join(upload_folder, test_file_name)

    with open(test_file_path, "wb") as file:
        file.write(test_file_content)

    try:
        response = client.delete(f"/delete_local_file/{test_file_name}")
        assert response.status_code == 200
        assert (
            response.json().get("message")
            == "The file has been successfully deleted from the local storage"
        )
        assert not os.path.exists(test_file_path)
    finally:
        if os.path.exists(test_file_path):
            os.remove(test_file_path)


def test_delete_nonexistent_local_file():
    response = client.delete("/delete_local_file/nonexistent_file.txt")
    assert response.status_code == 404


def test_list_local_files():
    create_test_file()
    try:
        response = client.get("/list_local_files")
        assert response.status_code == 200
        assert test_file_name in response.json().get("files")
    finally:
        remove_test_file()


def test_delete_from_s3(test_app, s3_mock):
    test_file_name = "testfile_to_delete.txt"
    s3_mock.put_object(
        Bucket="test-bucket", Key=f"folder/{test_file_name}", Body=b"test content"
    )

    response = test_app.delete(f"/delete_from_s3/{test_file_name}")
    assert response.status_code == 200
    assert response.json() == {
        "message": "The file has been successfully deleted from S3"
    }

    objects_in_bucket = s3_mock.list_objects(Bucket="test-bucket")
    filenames = [obj["Key"] for obj in objects_in_bucket.get("Contents", [])]
    assert f"folder/{test_file_name}" not in filenames


def test_delete_nonexistent_from_s3(test_app, s3_mock):
    response = test_app.delete("/delete_from_s3/nonexistent_file.txt")
    assert response.status_code == 200
    assert response.json() == {
        "message": "The file has been successfully deleted from S3"
    } or response.json() == {"detail": "An error occurred"}


def test_list_s3_files_empty(test_app, s3_mock):
    response = test_app.get("/list_s3_files")
    assert response.status_code == 200
    assert response.json().get("files") == []


def test_list_s3_files(test_app, s3_mock):
    s3_mock.put_object(
        Bucket="test-bucket", Key="folder/testfile.txt", Body=b"test content"
    )
    response = test_app.get("/list_s3_files")
    assert response.status_code == 200
    assert "testfile.txt" in response.json().get("files")
