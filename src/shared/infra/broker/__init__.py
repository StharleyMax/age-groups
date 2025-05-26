"""Defines the interface for message publishing and handling."""

from abc import ABC, abstractmethod


class MessageBroker(ABC):
    """Interface for message publishing."""

    @abstractmethod
    def publish(self, queue: str, message: dict, **kwargs):
        """Publish messages to a queue."""

    def consume(self, message: dict, **kwargs):
        """Consume messages."""
