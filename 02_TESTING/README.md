# Testing and Evaluation

`flow-tests.json` contains the automated route coverage, including edge cases. Run:

```bash
python generate-eval-dataset.py --tests-json flow-tests.json
```

The script should produce `output_eval_dataset.jsonl`. Place the actual generated file in this folder before final submission.

Then upload the JSONL to the evaluation S3 bucket, create the Bedrock Evaluation job, and capture the completed results page as:

`../03_EVIDENCE/12_bedrock_evaluation_results.png`

Do not create a fictional evaluation score. The score in the final submission must come from the AWS Evaluation job.
