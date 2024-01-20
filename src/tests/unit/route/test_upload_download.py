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


import docker

# import time


@pytest.fixture(scope="session")
def localstack_container():
    client = docker.from_env()
    container = client.containers.run(
        "localstack/localstack",
        ports={"4566": "4566"},
        detach=True,
        remove=True,
        environment={
            "SERVICES": "s3",
            "DEFAULT_REGION": "us-east-1",
            "AWS_ACCESS_KEY_ID": "test",
            "AWS_SECRET_ACCESS_KEY": "test",
        },
    )

    # time.sleep(10)

    yield

    container.stop()


@pytest.fixture(scope="function")
def s3_client(localstack_container):
    import boto3

    yield boto3.client(
        "s3",
        endpoint_url="http://localhost:4566",
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )


@pytest.fixture(scope="function")
def test_app_localstack(s3_client):
    os.environ["S3_BUCKET_NAME"] = "test-bucket"
    os.environ["USE_LOCALSTACK"] = "true"
    client = TestClient(main.app)
    yield client
    del os.environ["USE_LOCALSTACK"]


def test_s3_client_configuration(s3_client):
    assert s3_client.meta.endpoint_url == "http://localhost:4566"


def test_upload_to_s3_localstack(test_app_localstack, s3_client):
    s3_client.create_bucket(Bucket="test-bucket")

    response = s3_client.list_buckets()
    buckets = [bucket["Name"] for bucket in response["Buckets"]]
    assert "test-bucket" in buckets

    response = test_app_localstack.post(
        "/uploads3/", files={"file": ("testfile.txt", b"test content", "text/plain")}
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "The file has been successfully uploaded to S3"
    }

    objects_in_bucket = s3_client.list_objects(Bucket="test-bucket")
    filenames = [obj["Key"] for obj in objects_in_bucket.get("Contents", [])]

    assert "folder/testfile.txt" in filenames


import boto3

from moto import mock_s3


from moto import mock_ec2


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

    # TODO: ressurect logging
    # TODO: formularz
    # TODO: baza postgres, lokalna i na serwerze
    # TODO: setup na azure
    # TODO: podkladka pod tool do ML
    # TODO: podkladka do finansow
