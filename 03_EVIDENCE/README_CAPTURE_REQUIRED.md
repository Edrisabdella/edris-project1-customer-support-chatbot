# AWS Evidence Capture — Required Before Submission

This folder is reserved for **real screenshots captured from the student's AWS/Vocareum environment**

Required evidence files:

1. `01_full_flow_diagram.png` — Bedrock Flow showing classifier/prompt, Condition node, and three distinct Output paths.
2. `02_classifier_prompt.png` — classifier Prompt node configuration showing the allowed structured categories.
3. `03_condition_node_expressions.png` — Condition node expressions showing routing for BUG_REPORT, PLATFORM_QUESTION, and OTHER_REQUEST.
4. `04_flow_details.png` — optional but recommended Flow details/status evidence.
5. `05_bug_report_chat_transcript.png` — `chat.py` multi-turn conversation showing collection of description, reproduction steps, environment, tool call, and returned ticket ID.
6. `06_bug_report_tool_call.png` — close-up of `bugreports___create_bug_report` tool call and arguments.
7. `07_dynamodb_ticket.png` — DynamoDB `bug-report-tool-stack-bug-reports` table showing a ticket created by the chatbot.
8. `08_faq_prompt_node.png` — FAQ Prompt node configuration/template with the FAQ content or Knowledge Base retrieval configuration used by the final implementation.
9. `09_flow_test_faq_covered.png` — covered FAQ question and response.
10. `10_flow_test_faq_uncovered.png` — uncovered platform question and hand-off response.
11. `11_flow_test_other_request.png` — other-request hand-off response.
12. `12_bedrock_evaluation_results.png` — actual Bedrock Evaluation job results page, including the correctness score.

## Important

The project source and test definitions can be prepared locally, but the screenshots above must be captured after running the resources in AWS. The Bedrock Evaluation screenshot and `output_eval_dataset.jsonl` must reflect an actual run; no score should be invented.
