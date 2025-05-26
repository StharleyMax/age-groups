import threading
import time

import pytest
from fastapi.testclient import TestClient
from httpx import Response

import processor


class TestEnrollmentProcessor:
    """Test suite for the enrollment processor."""

    @pytest.fixture
    def enrollment(self) -> dict:
        """Fixture to provide enrollment data."""
        return {"name": "string", "age": 1, "cpf": "68676928198"}

    @pytest.fixture
    def new_enrollment(self, enrollment: dict, client: TestClient) -> Response:
        """Fixture to provide new enrollment data."""
        return client.post("/api/enrollments", json=enrollment)

    @pytest.fixture(autouse=True)
    def processor(self):
        """Fixture to mock the enrollment processor."""
        threading.Thread(target=processor.main, daemon=True).start()

    def test_process_enrollment(self, new_enrollment: Response, client: TestClient):
        """Test the enrollment processor."""
        time.sleep(4)
        enrollment_data = new_enrollment.json()
        response = client.get(f"/api/enrollments/{enrollment_data['cpf']}")

        assert response.json()["status"] != enrollment_data["status"]
