"""Test cases to verify the functionality of the AgeGroup endpoint."""

from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient


class TestAgeGroupEndpoint:
    """Test cases for the AgeGroup endpoint."""

    @pytest.fixture
    def age_group_data(self) -> dict:
        """Fixture to provide sample age group data."""
        return {"age_group": "18-24", "description": "Young Adult"}

    def test_create_age_group(self, client: TestClient, age_group_data: dict):
        """Test creating a new age group."""
        response = client.post("/api/age-groups/", json=age_group_data)
        assert response.status_code == HTTPStatus.CREATED.value
        assert response.json() == age_group_data
