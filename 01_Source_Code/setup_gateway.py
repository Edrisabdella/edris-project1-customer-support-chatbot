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

import json
from pathlib import Path

CONFIG = Path("agentcore_config.json")


def main():
    print("AgentCore Gateway setup")
    print("1. Deploy cloudformation-tool.yaml in us-east-1.")
    print("2. Register the Lambda target as 'bugreports'.")
    print("3. Expose create_bug_report to the harness.")
    print("4. Save the gateway/role identifiers in agentcore_config.json.")
    if CONFIG.exists():
        print(f"Existing configuration found: {CONFIG}")
    else:
        print("No configuration file exists yet; create it from the workspace setup output.")


if __name__ == "__main__":
    main()
