"""Dependencies for the application."""

from src.domains.enrollments.services.enrollment_service import EnrollmentService
from src.shared.infra.broker.sqs import SQSBroker


def get_enrollment_service() -> EnrollmentService:
    """Enrollment service dependency."""
    return EnrollmentService(broker=SQSBroker())
