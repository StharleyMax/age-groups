"""AgeGroupRepository class for interacting with DynamoDB."""

import uuid

from src.shared.infra.database.dynamodb import DynamoDB


class AgeGroupRepository:
    """Repository class for managing age groups in DynamoDB."""

    def __init__(self):
        self.table = DynamoDB().get_table("AgeGroups")

    def create(self, item: dict):
        """Create an item in the DynamoDB table."""
        payload = {**item, "id": str(uuid.uuid4())}
        self.table.put_item(Item=payload)
        return payload

    def get(self, key: dict):
        """Get an item from the DynamoDB table."""
        response = self.table.get_item(Key=key)
        return response.get("Item")

    def list(self):
        """List all items in the DynamoDB table."""
        response = self.table.scan()
        return response.get("Items", [])

    def delete(self, key: dict):
        """Delete an item from the DynamoDB table."""
        self.table.delete_item(Key=key)

    def age_range(self, age: int):
        """Get the age range for a specific age group."""
        response = self.table.scan(
            FilterExpression="min_age <= :age AND max_age >= :age",
            ExpressionAttributeValues={":age": age},
            Limit=1,
        )
        return response.get("Items", [])
