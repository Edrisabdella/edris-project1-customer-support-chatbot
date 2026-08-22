"""
Evaluation dataset generator.

The final harness invocation is intentionally isolated behind invoke_harness().
Connect that function to the AgentCore managed-harness session API available
in the Udacity workspace.
"""

import json
from pathlib import Path

TESTS = Path("harness-tests.json")
OUTPUT = Path("eval-dataset.jsonl")


def invoke_harness(test_input: str) -> str:
    raise NotImplementedError(
        "Connect invoke_harness() to the course workspace AgentCore harness API."
    )


def main():
    data = json.loads(TESTS.read_text(encoding="utf-8"))
    with OUTPUT.open("w", encoding="utf-8") as f:
        for test in data["tests"]:
            try:
                output = invoke_harness(test["input"])
                status = "generated"
            except NotImplementedError:
                output = ""
                status = "connect_harness_api"
            record = {
                "id": test["id"],
                "route": test["route"],
                "input": test["input"],
                "expected": test["expected"],
                "output": output,
                "status": status,
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
