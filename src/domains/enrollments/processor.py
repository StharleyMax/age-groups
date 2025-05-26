"""Enrollment processor for handling messages."""

from functools import cached_property

from src.domains.enrollments.services.enrollment_service import EnrollmentService
from src.shared.infra.broker.base_handler import BaseHandler


class EnrollmentHandler(BaseHandler):
    """Process enrollment messages."""

    queue = "enrollment-queue"

    @cached_property
    def service(self) -> EnrollmentService:
        """Return the service instance."""
        return EnrollmentService(self.broker)

    def handle(self, message: dict):
        """
        Broker handler for processing messages.

        :param message: Message containing enrollment data.
        """
        self.service.process_enrollment(message)
