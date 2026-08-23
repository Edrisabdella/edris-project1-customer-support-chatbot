import json
import os
import unittest
from unittest.mock import Mock, patch


class CreateBugReportTests(unittest.TestCase):
    def test_lambda_persists_complete_report_and_returns_open_ticket(self):
        os.environ["TABLE_NAME"] = "test-bug-reports"
        import create_bug_report

        table = Mock()
        event = {
            "messageVersion": "1.0",
            "function": "create_bug_report",
            "actionGroup": "bugreports",
            "parameters": [
                {"name": "description", "value": "Checkout crashes."},
                {"name": "stepsToReproduce", "value": "Click Pay."},
                {"name": "environment", "value": "Chrome on macOS."},
            ],
        }

        with patch.object(create_bug_report.boto3, "resource") as resource:
            resource.return_value.Table.return_value = table
            response = create_bug_report.lambda_handler(event, None)

        body = json.loads(response["response"]["functionResponse"]["responseBody"]["TEXT"]["body"])
        self.assertRegex(body["ticketId"], r"^[0-9a-f-]{36}$")
        self.assertEqual(body["status"], "OPEN")
        table.put_item.assert_called_once()
        item = table.put_item.call_args.kwargs["Item"]
        self.assertEqual(item["description"], "Checkout crashes.")
        self.assertEqual(item["status"], "OPEN")

    def test_lambda_rejects_missing_fields_without_persisting(self):
        os.environ["TABLE_NAME"] = "test-bug-reports"
        import create_bug_report

        event = {
            "messageVersion": "1.0",
            "function": "create_bug_report",
            "parameters": [{"name": "description", "value": "Only a description."}],
        }
        with patch.object(create_bug_report.boto3, "resource") as resource:
            response = create_bug_report.lambda_handler(event, None)

        body = json.loads(response["response"]["functionResponse"]["responseBody"]["TEXT"]["body"])
        self.assertEqual(body, {"error": "missing", "field": "stepsToReproduce"})
        resource.assert_not_called()


if __name__ == "__main__":
    unittest.main()