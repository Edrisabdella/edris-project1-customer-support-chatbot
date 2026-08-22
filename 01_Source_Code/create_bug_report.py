import json
import os
import uuid
from datetime import datetime, timezone

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    """Persist a completed bug report in DynamoDB."""
    if not isinstance(event, dict):
        raise ValueError("Event must be a JSON object")

    required = ("description", "stepsToReproduce", "environment")
    missing = [key for key in required if not str(event.get(key, "")).strip()]
    if missing:
        return {
            "statusCode": 400,
            "error": f"Missing required fields: {', '.join(missing)}"
        }

    ticket_id = f"BUG-{uuid.uuid4().hex[:10].upper()}"
    item = {
        "ticketId": ticket_id,
        "description": str(event["description"]).strip(),
        "stepsToReproduce": str(event["stepsToReproduce"]).strip(),
        "environment": str(event["environment"]).strip(),
        "status": "OPEN",
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }

    table.put_item(Item=item)

    return {
        "ticketId": ticket_id,
        "status": "OPEN"
    }
