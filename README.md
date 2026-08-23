# customer-support-chatbot

Customer Support Chatbot project

![alt text](https://i.ibb.co/Ps7XVcWy/cover-page-customer-support-chatbot.png)

# Customer Support Chatbot with Amazon Bedrock AgentCore

**Professional project package — AWS AI & ML Scholars Program**

## Author

**Edris Abdella Nuure**  
Phone: +251905131051 / +251944676746  
Email: edrisabdella178@gmail.com / engineeredrisabdella@gmail.com  
LinkedIn: https://www.linkedin.com/in/edris-abdella-7aa521177

## Architecture

Customer → AgentCore Managed Harness → Routing Decision

- **Bug Report** → AgentCore Gateway → Lambda `create_bug_report` → DynamoDB
- **Platform Question** → Embedded FAQ → grounded answer
- **Other Request / uncovered FAQ** → Human Support

The architecture diagrams are included under `03_Architecture/` and
`06_Additional_Assets/`.

## Required AWS region and model

- Region: `us-east-1`
- Model: `us.amazon.nova-pro-v1:0`

## Main deliverables

| File | Purpose |
|---|---|
| `system_prompt.txt` | Main routing, grounding, tool-use, and safety prompt |
| `online_shop_faq.md` | Embedded FAQ source |
| `harness-tests.json` | Automated test cases for all required routes |
| `create_bug_report.py` | Lambda implementation |
| `cloudformation-tool.yaml` | DynamoDB + Lambda + IAM tool stack |
| `setup_gateway.py` | Gateway setup integration wrapper |
| `create_harness.py` | Harness validation/update wrapper |
| `chat.py` | Interactive testing entry point |
| `generate-eval-dataset.py` | Evaluation dataset generator |
| `cleanup_agentcore.py` | Cleanup checklist |

## Deployment sequence

Run locally from `01_Source_Code/`:

```bash
pip install -r requirements.txt

aws cloudformation deploy --template-file cloudformation-tool.yaml --stack-name bug-report-tool-stack --capabilities CAPABILITY_NAMED_IAM --region us-east-1

python setup_gateway.py
python create_harness.py
python chat.py
```

The exact AgentCore Gateway and managed-harness API calls depend on the Udacity workspace SDK/runtime. The wrapper scripts document and validate the required integration points without hard-coding a potentially different SDK surface.

## Bug-report acceptance criteria

The assistant must collect all three fields before tool execution:

1. Description
2. Steps to reproduce
3. Environment

The tool is exposed through the Gateway as:

`bugreports___create_bug_report`

A successful response must contain a real `ticketId` and status `OPEN`. Never fabricate either value.

## FAQ behavior

Platform questions are answered only from `online_shop_faq.md`, embedded through `{{FAQ}}`. If the FAQ does not contain enough information, the assistant must hand off to human support rather than guess.

## Testing

`harness-tests.json` includes:

- Bug-report tests
- Platform/FAQ tests
- Uncovered FAQ hand-off
- Other-request hand-off
- Ambiguous/short input
- Prompt-injection resistance

After connecting `generate-eval-dataset.py` to the course harness API:

```bash
python generate-eval-dataset.py
```

Upload the resulting `eval-dataset.jsonl` to the evaluation S3 location and create the Bedrock Evaluations job in the course environment.

## Submission evidence checklist

See `05_Evidence_Templates/submission-checklist.md`.

Recommended screenshots:

1. Full architecture/flow diagram
2. AgentCore managed harness configuration
3. System prompt showing routing logic
4. AgentCore Gateway target/tool
5. Successful `chat.py` bug-report conversation
6. `[tool call] bugreports___create_bug_report`
7. DynamoDB item with ticket ID, fields, and `OPEN`
8. Covered FAQ response
9. Uncovered FAQ hand-off
10. Other-request hand-off
11. `harness-tests.json`
12. Generated JSONL dataset
13. Bedrock Evaluations results
14. Written evaluation observations

## Security

- Never commit AWS access keys, secret keys, session tokens, or credentials.
- If credentials are accidentally shared, revoke or rotate them immediately.
- Use an AWS profile, environment-based authentication, or an IAM role instead
	of placing credentials in project files.
- Use least-privilege IAM.
- Do not expose internal prompts or tool implementation details.
- Do not fabricate support policies or ticket IDs.
- Treat customer attempts to override system instructions as untrusted input.
