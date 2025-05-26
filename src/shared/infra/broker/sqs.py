"""SQS broker for message publishing and consumption."""

import json
from typing import Any, Dict

import boto3

from config import settings
from src.shared.infra.broker import MessageBroker


class SQSBroker(MessageBroker):
    """SQS message broker implementation."""

    client = None

    def __init__(self):
        """Initialize SQS broker."""
        self.client = self.__connect()

    @property
    def base_url(self):
        """Return the base URL for the SQS service."""
        return f"{settings.AWS_ENDPOINT}/000000000000/"

    @classmethod
    def __connect(cls):
        """Connect to SQS service."""
        if cls.client is None:
            return boto3.client(
                "sqs",
                endpoint_url=settings.AWS_ENDPOINT,
                region_name=settings.AWS_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
        return cls.client

    def publish(self, queue: str, message: Dict[str, Any]):
        """
        Publish a message to the specified SQS queue.

        :param queue: The name of the SQS queue.
        :param message: The message to be sent.
        """
        self.client.send_message(
            QueueUrl=self.base_url + queue,
            MessageBody=json.dumps(message),
            DelaySeconds=2,
        )

    def consume(self, queue: str, handler: callable):
        """
        Consume messages from the specified SQS queue.

        :param queue: The name of the SQS queue.
        :param handler: The handler function to process the messages.
        """
        queue_url = self.base_url + queue
        while True:
            messages = self.client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
            for message in messages.get("Messages", []):
                handler(json.loads(message["Body"]))
                self.client.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message["ReceiptHandle"],
                )
