import argparse, json, pathlib, uuid, boto3

parser=argparse.ArgumentParser()
parser.add_argument("--tests-json",default="flow-tests.json")
args=parser.parse_args()

cfg=json.load(open("agentcore_config.json",encoding="utf-8"))
tests=json.load(open(args.tests_json,encoding="utf-8"))["tests"]
client=boto3.client("bedrock-agentcore",region_name="us-east-1")
rows=[]

for t in tests:
    try:
        r=client.invoke_harness(
            harnessArn=cfg["harnessArn"],
            runtimeSessionId=str(uuid.uuid4()),
            actorId="evaluation",
            messages=[{"role":"user","content":[{"text":t["prompt"]}]}],
            maxIterations=10,
        )
        actual=str(r)
    except Exception as exc:
        actual="[HARNESS_ERROR] "+repr(exc)
    rows.append({"prompt":t["prompt"],"referenceResponse":t["expected"],
                 "modelResponses":[{"response":actual,"modelIdentifier":"my-support-chatbot"}]})

pathlib.Path("output_eval_dataset.jsonl").write_text(
    "\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf-8")
print(f"Wrote {len(rows)} evaluation records to output_eval_dataset.jsonl")
