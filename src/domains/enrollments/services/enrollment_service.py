"""Enrollment service."""

import logging
import random

from src.shared.infra.broker import MessageBroker
from src.shared.infra.database.repository.age_group_repository import AgeGroupRepository
from src.shared.infra.database.repository.enrollment_repository import EnrollmentRepository


class EnrollmentService:
    """Service for enrollment business logic."""

    logger = logging.getLogger(__name__)

    enrollment_repo = EnrollmentRepository()
    age_group_repo = AgeGroupRepository()

    def __init__(self, broker: MessageBroker):
        self.broker = broker

    def create(self, enrollment: dict):
        """Create new enrollment with age validation."""
        age_range = self.age_group_repo.age_range(enrollment["age"])
        if not age_range:
            raise ValueError("Age does not match any registered age group")

        created_enrollment = self.enrollment_repo.create({
            **enrollment,
            "age_group_id": age_range[0]["id"],
        })
        try:
            self.broker.publish(queue="enrollment-queue", message=created_enrollment)
        except Exception:
            raise
        return created_enrollment

    def process_enrollment(self, enrollment_data: dict) -> dict:
        """
        Process enrollment data by simulating a status update.

        :param enrollment_data: Data containing enrollment information.
        """
        status = random.choice(["processed", "failed"])
        process = self.enrollment_repo.status_update(enrollment_data["cpf"], status)
        self.logger.info(
            "Enrollment for cpf %s processed with status %s",
            enrollment_data["cpf"],
            status,
        )
        return process

    def get(self, key: dict):
        """Get an enrollment by key."""
        return self.enrollment_repo.get(key)
