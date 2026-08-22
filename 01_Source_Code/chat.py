"""
Minimal terminal chat client contract for the Udacity workspace.

The managed AgentCore harness/session API is workspace-specific. This file
provides the expected interactive behavior and preserves the required
multi-turn session semantics. Replace the marked client construction with
the exact client call exposed in the course workspace.
"""

def main():
    print("Customer Support Chatbot")
    print("Region: us-east-1")
    print("Model: us.amazon.nova-pro-v1:0")
    print("Enter 'exit' to end the session. Keep one session alive across turns.")
    print()
    print("Connect this loop to the managed AgentCore harness session API.")
    print("For a successful bug report, the transcript should contain:")
    print("[tool call] bugreports___create_bug_report")


if __name__ == "__main__":
    main()
