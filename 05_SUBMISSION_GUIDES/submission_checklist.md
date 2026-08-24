# Final Submission Checklist

## Core rubric
- [ ] Full Bedrock Flow screenshot: Input → Classifier Prompt → Condition → three distinct Output nodes.
- [ ] Classifier prompt screenshot showing exactly `BUG_REPORT`, `PLATFORM_QUESTION`, `OTHER_REQUEST`.
- [ ] Condition-node screenshot showing the three routing expressions.
- [ ] `system_prompt.txt` submitted with bug collection rules.
- [ ] Bug conversation transcript showing follow-up questions.
- [ ] Transcript shows `bugreports___create_bug_report`.
- [ ] DynamoDB screenshot shows a real ticket record.
- [ ] FAQ prompt/configuration screenshot.
- [ ] Covered FAQ test response screenshot.
- [ ] Uncovered FAQ test response screenshot.
- [ ] Other-request hand-off screenshot.
- [ ] `flow-tests.json` submitted.
- [ ] `output_eval_dataset.jsonl` submitted.
- [ ] S3 upload completed.
- [ ] Bedrock Evaluation job created.
- [ ] Evaluation results screenshot.
- [ ] Written evaluation observations included.

## Stand-out enhancements
- [ ] Guardrail enabled before model processing where supported by the chosen deployment path.
- [ ] Ambiguous-message tests.
- [ ] Very-short-message tests.
- [ ] Prompt-injection tests.
- [ ] Multi-turn bug-report test.
- [ ] DynamoDB fields match the customer-provided values.
- [ ] FAQ extended with additional entries.
- [ ] Knowledge Base created and tested.
- [ ] Structured classifier output validated.
- [ ] No credentials or secrets committed to the project.

## Evidence naming
01_flow_full.png
02_classifier_prompt.png
03_condition_expressions.png
04_bug_chat_transcript.png
05_dynamodb_ticket.png
06_faq_answer.png
07_uncovered_handoff.png
08_other_request.png
09_eval_results.png
10_architecture.png
