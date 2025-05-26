"""Test cases for the enrollment endpoint."""

from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from httpx import Response


class TestEnrollmentEndpoint:
    """Test suite for the enrollment endpoint."""

    @pytest.fixture
    def enrollment(self) -> dict:
        """Fixture to provide enrollment data."""
        return {"name": "string", "age": 1, "cpf": "68676928198"}

    @pytest.fixture
    def new_enrollment(self, enrollment: dict, client: TestClient) -> Response:
        """Fixture to provide new enrollment data."""
        return client.post("/api/enrollments", json=enrollment)

    def test_enrollment_endpoint(self, new_enrollment, enrollment):
        """Test the enrollment endpoint."""
        enrollment_data = new_enrollment.json()
        assert new_enrollment.status_code == HTTPStatus.CREATED
        assert enrollment_data["name"] == enrollment["name"]
        assert enrollment_data["age"] == enrollment["age"]
        assert enrollment_data["cpf"] == enrollment["cpf"]
        assert enrollment_data["status"] == "pending"
        assert enrollment_data.get("age_group_id") is not None

    def test_enrollment_endpoint_get(self, new_enrollment: Response, client: TestClient):
        """Test retrieving the created enrollment."""
        enrollment_data = new_enrollment.json()
        response = client.get(f"/api/enrollments/{enrollment_data['cpf']}")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == enrollment_data
