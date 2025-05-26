"""Processor module for handling events."""

import threading

from src.domains.enrollments.processor import EnrollmentHandler
from src.shared.infra.broker.sqs import SQSBroker


def main():
    """Start the enrollment processor."""
    broker = SQSBroker()
    threading.Thread(
        target=broker.consume,
        args=(EnrollmentHandler.queue, EnrollmentHandler(broker)),
        daemon=True,
    ).start()


if __name__ == "__main__":
    main()
