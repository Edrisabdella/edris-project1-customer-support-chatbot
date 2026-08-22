# Professional Submission Checklist

## Architecture
- [ ] Architecture diagram included
- [ ] Customer → AgentCore → routing paths are visible
- [ ] Gateway → Lambda → DynamoDB path is visible
- [ ] FAQ grounding path is visible
- [ ] Human support hand-off is visible

## Classification and routing
- [ ] Exactly three routes are documented
- [ ] Bug reports route to bug collection
- [ ] Platform questions route to FAQ
- [ ] Other/uncovered requests route to human support

## Bug reports
- [ ] Description collected
- [ ] Steps to reproduce collected
- [ ] Environment collected
- [ ] Tool called only after all three are present
- [ ] Ticket ID returned from the real tool
- [ ] DynamoDB record exists with status OPEN

## FAQ
- [ ] FAQ embedded through {{FAQ}}
- [ ] Covered question tested
- [ ] Uncovered question tested
- [ ] No unsupported answers fabricated

## Testing and evaluation
- [ ] harness-tests.json completed
- [ ] eval-dataset.jsonl generated
- [ ] JSONL uploaded to S3
- [ ] Bedrock Evaluation job created
- [ ] Correctness score reviewed
- [ ] Observations written

## Security / edge cases
- [ ] Prompt injection tested
- [ ] Very short input tested
- [ ] Ambiguous input tested
- [ ] Secrets excluded from repository
