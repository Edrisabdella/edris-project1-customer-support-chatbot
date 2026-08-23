"""
Harness creation/update wrapper.

The Udacity workspace supplies the AgentCore managed-harness SDK/API.
This script documents the required inputs and performs validation before
the course-specific harness creation command is executed.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PROMPT = ROOT / "system_prompt.txt"
FAQ = ROOT / "online_shop_faq.md"
CONFIG = ROOT / "agentcore_config.json"


def main():
    assert PROMPT.exists(), "system_prompt.txt is missing"
    assert FAQ.exists(), "online_shop_faq.md is missing"
    assert CONFIG.exists(), "Run setup_gateway.py --write-template and fill agentcore_config.json first"

    try:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SystemExit(f"Invalid JSON in {CONFIG}: {error}")
    for key in ("gatewayIdentifier", "gatewayRoleArn"):
        if not str(config.get(key, "")).strip() or str(config[key]).startswith("REPLACE_WITH_"):
            raise SystemExit(f"Set a real non-secret {key} in {CONFIG}")

    prompt = PROMPT.read_text(encoding="utf-8")
    faq = FAQ.read_text(encoding="utf-8")
    assert "{{FAQ}}" in prompt, "Keep the {{FAQ}} placeholder in system_prompt.txt"
    final_prompt = prompt.replace("{{FAQ}}", faq)

    print("Prompt validation successful.")
    print(f"Final prompt length: {len(final_prompt):,} characters")
    print("Use the Udacity workspace AgentCore managed-harness creation API")
    print("with model: us.amazon.nova-pro-v1:0 and region: us-east-1.")
    print(f"Gateway identifier: {config['gatewayIdentifier']}")
    print("The harness must be configured to invoke the AgentCore Gateway.")


if __name__ == "__main__":
    main()
