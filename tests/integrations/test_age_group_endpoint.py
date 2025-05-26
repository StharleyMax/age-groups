"""Test suite for the age group endpoint."""

import base64
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from httpx import Response

from config import settings


class TestAgeGroupEndpoint:
    """Test suite for the age group endpoint."""

    @pytest.fixture
    def age_group(self) -> dict:
        """Fixture to provide age group data."""
        return {"min_age": 0, "max_age": 15}

    @pytest.fixture
    def auth_headers(self) -> dict:
        """Fixture to provide authentication headers."""
        credentials = f"{settings.USERNAME}:{settings.PASSWORD}"
        credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        return {"Authorization": f"Basic {credentials}"}

    @pytest.fixture
    def new_age_group(self, age_group: dict, client: TestClient, auth_headers: dict) -> Response:
        """Fixture to provide new age group data."""
        return client.post("/api/age-groups", json=age_group, headers=auth_headers)

    def test_age_group_endpoint_create(self, new_age_group: dict, age_group: dict):
        """Test creating a new age group."""
        age_group_data = new_age_group.json()
        assert new_age_group.status_code == HTTPStatus.CREATED
        assert age_group_data["min_age"] == age_group["min_age"]
        assert age_group_data["max_age"] == age_group["max_age"]
        assert age_group_data.get("id") is not None

    def test_age_group_endpoint_get(
        self,
        new_age_group: dict,
        client: TestClient,
        auth_headers: dict,
    ):
        """Test retrieving the created age group."""
        age_group_data = new_age_group.json()
        response = client.get(f"/api/age-groups/{age_group_data['id']}", headers=auth_headers)
        assert response.status_code == HTTPStatus.OK
        assert response.json() == age_group_data

    def test_age_group_endpoint_delete(
        self,
        new_age_group: dict,
        client: TestClient,
        auth_headers: dict,
    ):
        """Test deleting the created age group."""
        age_group_data = new_age_group.json()
        response = client.delete(f"/api/age-groups/{age_group_data['id']}", headers=auth_headers)
        assert response.status_code == HTTPStatus.NO_CONTENT

        response = client.get(f"/api/age-groups/{age_group_data['id']}", headers=auth_headers)
        assert response.status_code == HTTPStatus.NOT_FOUND
