import pytest
from typing import Generator
from starlette.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from app.setup import create_app


@pytest.fixture()
def client() -> Generator:
    app = create_app()
    initializer(["app.models"], "sqlite://:memory:")
    with TestClient(app) as c:
        yield c
    finalizer()


@pytest.fixture()
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()
