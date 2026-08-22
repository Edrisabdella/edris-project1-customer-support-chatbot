"""
Harness creation/update wrapper.

The Udacity workspace supplies the AgentCore managed-harness SDK/API.
This script documents the required inputs and performs validation before
the course-specific harness creation command is executed.
"""

from pathlib import Path
import json

PROMPT = Path("system_prompt.txt")
FAQ = Path("online_shop_faq.md")
CONFIG = Path("agentcore_config.json")


def main():
    assert PROMPT.exists(), "system_prompt.txt is missing"
    assert FAQ.exists(), "online_shop_faq.md is missing"
    assert CONFIG.exists(), "Run setup_gateway.py and create agentcore_config.json first"

    prompt = PROMPT.read_text(encoding="utf-8")
    faq = FAQ.read_text(encoding="utf-8")
    assert "{{FAQ}}" in prompt, "Keep the {{FAQ}} placeholder in system_prompt.txt"
    final_prompt = prompt.replace("{{FAQ}}", faq)

    print("Prompt validation successful.")
    print(f"Final prompt length: {len(final_prompt):,} characters")
    print("Use the Udacity workspace AgentCore managed-harness creation API")
    print("with model: us.amazon.nova-pro-v1:0 and region: us-east-1.")
    print("The harness must be configured to invoke the AgentCore Gateway.")


if __name__ == "__main__":
    main()
