"""Enrollment processor for handling messages."""

from abc import ABC, abstractmethod

from src.shared.infra.broker import MessageBroker


class BaseHandler(ABC):
    """
    Process enrollment messages.

    Base class for handling messages from a broker service.
    """

    def __init__(self, broker: MessageBroker):
        self.broker = broker

    def __call__(self, message: dict):
        """
        Make the class callable and process a message.

        :param message: Message to be processed.
        """
        self.handle(message)

    @abstractmethod
    def handle(self, message: dict):
        """Broker handler for processing messages."""
