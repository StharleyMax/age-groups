"""Test client fixture for FastAPI."""

import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from src.app import create_app


@pytest.fixture
def client(mocker: MockerFixture) -> TestClient:
    """Fixture to return a FastAPI test client."""
    return TestClient(create_app())
