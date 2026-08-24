# Professional Submission Checklist

## Architecture
- [x] Architecture diagram included
- [x] Customer → AgentCore → routing paths are visible in the architecture specification
- [x] Gateway → Lambda → DynamoDB path is visible
- [x] FAQ grounding path is visible
- [x] Human support hand-off is visible
- [ ] Capture and attach full Bedrock Flow diagram screenshot
- [ ] Capture and attach classifier prompt configuration screenshot
- [ ] Capture and attach Condition node expressions screenshot

## Classification and routing
- [x] Exactly three routes are documented
- [x] Bug reports route to bug collection
- [x] Platform questions route to FAQ
- [x] Other/uncovered requests route to human support
- [x] Flow node and condition specification included in `03_Architecture/flow-routing-spec.md`

## Bug reports
- [x] Description collected
- [x] Steps to reproduce collected
- [x] Environment collected
- [x] Tool called only after all three are present
- [x] Ticket ID returned in local deterministic test; AWS ticket requires live run
- [ ] Attach `chat.py` AWS transcript showing the tool call
- [ ] Attach DynamoDB screenshot showing an item with status OPEN

## FAQ
- [x] FAQ embedded through {{FAQ}}
- [x] Covered question tested
- [x] Uncovered question tested
- [x] No unsupported answers fabricated
- [ ] Attach FAQ Prompt node screenshot from the deployed Flow

## Testing and evaluation
- [x] `flow-tests.json` completed
- [x] `eval-dataset.jsonl` generated as a local evaluation artifact
- [ ] JSONL uploaded to S3
- [ ] Bedrock Evaluation job created
- [ ] Correctness score reviewed
- [x] Observations and limitations written
- [ ] Attach Bedrock Evaluation results screenshot

## Security / edge cases
- [x] Prompt injection tested
- [x] Very short input tested
- [x] Ambiguous input tested
- [x] Secrets excluded from repository

## Evidence files

See `evidence-register.md` for the exact filenames and capture instructions
required before final submission.
