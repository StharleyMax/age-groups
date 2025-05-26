"""Processor module for handling events."""

from src.domains.enrollments.processor import EnrollmentHandler
from src.shared.infra.broker.sqs import SQSBroker


def main():
    """Start the enrollment processor."""
    broker = SQSBroker()
    broker.consume(EnrollmentHandler.queue, EnrollmentHandler(broker))


if __name__ == "__main__":
    main()
