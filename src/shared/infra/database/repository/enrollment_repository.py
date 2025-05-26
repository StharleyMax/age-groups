"""Enrollment Repository Module."""

from datetime import datetime

from src.shared.infra.database.dynamodb import DynamoDB


class EnrollmentRepository:
    """Repository for managing enrollments in DynamoDB."""

    def __init__(self):
        self.table = DynamoDB().get_table("Enrollments")

    def create(self, enrollment_data: dict):
        """Create a new enrollment."""
        enrollment = {
            "cpf": enrollment_data["cpf"],
            "name": enrollment_data["name"],
            "age": int(enrollment_data["age"]),
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "age_group_id": enrollment_data.get("age_group_id", ""),
        }

        self.table.put_item(Item=enrollment)
        return enrollment

    def get(self, key: dict):
        """Get enrollment by CPF."""
        response = self.table.get_item(Key=key)
        return response.get("Item")

    def status_update(self, cpf: str, status: str):
        """Update enrollment status."""
        self.table.update_item(
            Key={"cpf": cpf},
            UpdateExpression="SET #status = :status, updated_at = :now",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={":status": status, ":now": datetime.now().isoformat()},
            ReturnValues="ALL_NEW",
        )

    def list_by_status(self, status: str):
        """List enrollments by status using GSI."""
        response = self.table.query(
            IndexName="StatusIndex",
            KeyConditionExpression="status = :status",
            ExpressionAttributeValues={":status": status},
        )
        return response.get("Items", [])
