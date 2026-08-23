#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

import boto3


def invoke_flow_once(
    client,
    flow_identifier: str,
    flow_alias_identifier: str,
    input_node_name: str,
    prompt: str,
    enable_trace: bool = False,
) -> Dict[str, Any]:
    """
    Invokes a Bedrock Flow and returns:
      {
        "executionId": "...",
        "final_output_text": "...",
        "final_output_raw": <document>,
        "trace": <optional list of trace events>
      }
    """
    resp = client.invoke_flow(
        flowIdentifier=flow_identifier,
        flowAliasIdentifier=flow_alias_identifier,
        enableTrace=enable_trace,
        inputs=[
            {
                "nodeName": input_node_name,
                "nodeOutputName": "document",
                "content": {"document": prompt},
            }
        ],
    )

    last_text_any = None

    for event in resp["responseStream"]:
        if "flowOutputEvent" in event:
            oe = event["flowOutputEvent"]
            last_text_any = oe.get("content", {}).get("document")
            break

        if "flowMultiTurnInputRequestEvent" in event:
            ce = event["flowMultiTurnInputRequestEvent"]
            last_text_any = ce.get("content", {}).get("document")
            break

    return {
        "final_output_text": last_text_any,
    }


def main():
    p = argparse.ArgumentParser(description="Run Bedrock Flow tests and emit Bedrock Evaluations JSONL (LLM-as-judge BYOI).")
    p.add_argument("--tests-json", default="harness-tests.json", help="Path to the test suite JSON.")
    p.add_argument("--flow-id", help="Bedrock Flow identifier (required unless --dry-run is used).")
    p.add_argument("--flow-alias-id", help="Bedrock Flow alias identifier (required unless --dry-run is used).")
    p.add_argument("--model-identifier", default="my-flow-app", help="Value to put in modelResponses[0].modelIdentifier.")
    p.add_argument("--out-jsonl", default="output_eval_dataset.jsonl", help="Where to write the eval dataset JSONL.")
    p.add_argument("--region", default=None, help="AWS region (optional; otherwise uses default boto config).")
    p.add_argument("--enable-trace", action="store_true", help="Include trace collection (not written to eval JSONL).")
    p.add_argument("--dry-run", action="store_true", help="Create an evaluation template without invoking AWS.")
    args = p.parse_args()

    if not args.dry_run and (not args.flow_id or not args.flow_alias_id):
        p.error("--flow-id and --flow-alias-id are required unless --dry-run is used")

    suite = json.loads(Path(args.tests_json).read_text(encoding="utf-8"))
    input_node_name = suite.get("flowInputNode", {}).get("nodeName", "FlowInputNode")

    print("Input node name: " + input_node_name)

    tests = suite["tests"]

    client = None
    if not args.dry_run:
        session = boto3.Session(region_name=args.region) if args.region else boto3.Session()
        client = session.client("bedrock-agent-runtime")

    out_path = Path(args.out_jsonl)
    n_ok = 0

    with out_path.open("w", encoding="utf-8") as f:
        for t in tests:
            test_id = t["id"]
            reference = t.get("expected", "")
            prompt = t.get("prompt", t.get("input", ""))

            if args.dry_run:
                response_text = "[NOT_INVOKED] Run without --dry-run after configuring the Bedrock Flow."
            else:
                try:
                    result = invoke_flow_once(
                        client=client,
                        flow_identifier=args.flow_id,
                        flow_alias_identifier=args.flow_alias_id,
                        input_node_name=input_node_name,
                        prompt=prompt,
                        enable_trace=args.enable_trace,
                    )
                    response_text = result["final_output_text"]
                    n_ok += 1
                except Exception as e:
                    # Keep a failure record so the evaluation run captures it.
                    print(f"{test_id}: {e}", file=sys.stderr)
                    response_text = f"[FLOW_ERROR] {type(e).__name__}: {e}"

            # Bedrock Evaluations LLM-as-a-judge (BYOI) input JSONL record
            record = {
                "prompt": prompt,
                "referenceResponse": reference,
                "modelResponses": [
                    {
                        "response": response_text,
                        "modelIdentifier": args.model_identifier,
                    }
                ],
                # Optional: keep the test id as metadata by embedding into the prompt or category,
                # since the public schema doesn't show a dedicated id field.
            }

            f.write(json.dumps(record, ensure_ascii=False) + "\n")

            print(f"{test_id}: wrote eval line", file=sys.stderr)

    print(f"\nWrote {len(tests)} JSONL lines to {out_path} ({n_ok} flow calls succeeded).", file=sys.stderr)


if __name__ == "__main__":
    main()