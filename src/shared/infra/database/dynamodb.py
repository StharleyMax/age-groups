"""DynamoDB connection."""

import boto3

from config import settings
from src.shared.singleton import SingletonMeta


class DynamoDB(metaclass=SingletonMeta):
    """Singleton class to manage DynamoDB connection."""

    def __init__(self):
        """Initialize the DynamoDB connection."""
        self.resource = boto3.resource(
            "dynamodb",
            endpoint_url=settings.AWS_ENDPOINT,
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    def get_table(self, table_name: str):
        """Get a DynamoDB table."""
        return self.resource.Table(table_name)
