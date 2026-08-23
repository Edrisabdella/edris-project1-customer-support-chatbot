import json
import os
import uuid
from datetime import datetime, timezone
import boto3

REQUIRED_FIELDS = ("description", "stepsToReproduce", "environment")

def lambda_handler(event, _):
    if not isinstance(event, dict):
        return _resp({}, {"error": "invalid_event"})

    print("EVENT:", json.dumps(event, indent=2, default=str))

    if event.get("messageVersion") != "1.0" or event.get("function") != "create_bug_report":
        return _resp(event, {"error": "unsupported"})

    params = event.get("parameters") or []
    body = {
        p.get("name"): p.get("value")
        for p in params
        if isinstance(p, dict) and p.get("name") is not None
    }

    description = (body.get("description") or "").strip()
    steps = (body.get("stepsToReproduce") or "").strip()
    environment = (body.get("environment") or "").strip()

    missing = [
        field
        for field, value in (
            ("description", description),
            ("stepsToReproduce", steps),
            ("environment", environment),
        )
        if not value
    ]
    if missing:
        return _resp(event, {"error": "missing", "field": missing[0]})

    ticket_id = str(uuid.uuid4())
    item = {
        "ticketId": ticket_id,
        "description": description,
        "stepsToReproduce": steps,
        "environment": environment,
        "status": "OPEN",
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }

    boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"]).put_item(Item=item)

    return _resp(event, {"ticketId": ticket_id, "status": "OPEN"})


def _resp(event, obj):
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": event.get("actionGroup"),
            "function": event.get("function"),
            "functionResponse": {
                "responseBody": {
                    "TEXT": {
                        "body": json.dumps(obj)
                    }
                }
            },
        },
    }