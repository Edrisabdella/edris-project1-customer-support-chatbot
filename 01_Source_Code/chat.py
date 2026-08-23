"""Run the customer-support chatbot locally for an end-to-end smoke test."""

from pathlib import Path

from support_bot import SupportAssistant


FAQ_PATH = Path(__file__).with_name("online_shop_faq.md")

def main():
    print("Customer Support Chatbot")
    print("Local mode: no AWS credentials required")
    print("Enter 'exit' to end the session.")
    print()
    assistant = SupportAssistant(FAQ_PATH.read_text(encoding="utf-8"))

    while True:
        try:
            message = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if message.lower() == "exit":
            break
        if not message:
            continue
        print(f"Assistant: {assistant.respond(message)}")
        if assistant.last_tool_call:
            print(f"[tool call] {assistant.last_tool_call}")
            assistant.last_tool_call = None


if __name__ == "__main__":
    main()
