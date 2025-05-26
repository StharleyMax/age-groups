"""Enrollment processor for handling messages."""

import logging
from functools import cached_property

from src.domains.enrollments.services.enrollment_service import EnrollmentService
from src.shared.infra.broker.base_handler import BaseHandler


class EnrollmentHandler(BaseHandler):
    """Process enrollment messages."""

    logger = logging.getLogger(__name__)

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
        self.logger.info("Processing enrollment to cpf: %s", message["cpf"])
        self.service.process_enrollment(message)
