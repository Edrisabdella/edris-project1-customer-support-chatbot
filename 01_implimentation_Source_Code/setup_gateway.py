"""
AgentCore Gateway setup entry point.

This file is intentionally kept as a project-side integration wrapper.
Run it in the Udacity workspace after cloudformation-tool.yaml has been
deployed. The course-provided AgentCore Gateway SDK/API should be used to
register the Lambda target as:

    target: bugreports
    tool:   bugreports___create_bug_report

The exact AgentCore SDK surface can vary by course workspace/runtime.
Keep the generated agentcore_config.json in the starter directory and
never commit credentials or secrets.
"""

import argparse
import json
from pathlib import Path

CONFIG = Path(__file__).resolve().parent / "agentcore_config.json"
EXAMPLE = Path(__file__).resolve().parent / "agentcore_config.example.json"


def write_template() -> None:
    if CONFIG.exists():
        raise FileExistsError(f"Refusing to overwrite existing configuration: {CONFIG}")
    CONFIG.write_text(EXAMPLE.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Created configuration template: {CONFIG}")
    print("Fill in identifiers only; authenticate with an AWS profile or environment outside this file.")


def main():
    parser = argparse.ArgumentParser(description="Prepare non-secret AgentCore Gateway configuration.")
    parser.add_argument("--write-template", action="store_true", help="Create agentcore_config.json from the safe template.")
    args = parser.parse_args()

    if args.write_template:
        write_template()
        return

    print("AgentCore Gateway setup")
    print("1. Deploy cloudformation-tool.yaml in us-east-1.")
    print("2. Register the Lambda target as 'bugreports'.")
    print("3. Expose create_bug_report to the harness.")
    print("4. Save the gateway/role identifiers in agentcore_config.json.")
    if CONFIG.exists():
        try:
            config = json.loads(CONFIG.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise SystemExit(f"Invalid JSON in {CONFIG}: {error}")
        missing = [key for key in ("gatewayIdentifier", "gatewayRoleArn") if not str(config.get(key, "")).strip()]
        if missing:
            raise SystemExit(f"Configuration is missing: {', '.join(missing)}")
        print(f"Existing configuration found: {CONFIG}")
        print("Non-secret Gateway identifiers are present.")
    else:
        print("No configuration file exists yet; create it from the workspace setup output.")


if __name__ == "__main__":
    main()
