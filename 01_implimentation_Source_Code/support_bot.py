"""Small dependency-free local implementation of the documented support flow."""

import re
import uuid
from dataclasses import dataclass, field


SUPPORT_PHONES = ("+251905131051", "+251944676746")


@dataclass
class SupportAssistant:
    faq: str
    bug_fields: dict[str, str] = field(default_factory=dict)
    last_tool_call: str | None = None

    def respond(self, message: str) -> str:
        self.last_tool_call = None
        text = message.strip()
        lower = text.lower()

        if self.bug_fields:
            self._capture_bug_fields(text)
            missing = self._missing_bug_field()
            if missing:
                return self._bug_question(missing)
            return self._create_bug_report()

        if self._is_injection(lower):
            return self._handoff("I can help with online-shop support, but I cannot reveal internal instructions.")

        if self._is_bug(lower):
            self.bug_fields["description"] = text
            self._capture_bug_fields(text, allow_fallback=False)
            missing = self._missing_bug_field()
            return self._bug_question(missing) if missing else self._create_bug_report()

        if self._is_platform_question(lower):
            return self._answer_faq(lower)

        return self._handoff()

    def _capture_bug_fields(self, text: str, allow_fallback: bool = True) -> None:
        patterns = {
            "description": r"(?:description|problem|issue)\s*:\s*(.+?)(?=\s+(?:steps?|environment)\s*:|$)",
            "stepsToReproduce": r"(?:steps?|steps to reproduce)\s*:\s*(.+?)(?=\s+environment\s*:|$)",
            "environment": r"environment\s*:\s*(.+)$",
        }
        for field_name, pattern in patterns.items():
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                self.bug_fields[field_name] = match.group(1).strip()

        missing = self._missing_bug_field()
        if allow_fallback and missing and not any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns.values()):
            self.bug_fields[missing] = text

    def _missing_bug_field(self) -> str | None:
        for field_name in ("description", "stepsToReproduce", "environment"):
            if not self.bug_fields.get(field_name, "").strip():
                return field_name
        return None

    @staticmethod
    def _bug_question(field_name: str | None) -> str:
        questions = {
            "stepsToReproduce": "What steps reproduce the problem?",
            "environment": "What browser, device, operating system, or app version are you using?",
        }
        return questions[field_name] if field_name else ""

    def _create_bug_report(self) -> str:
        ticket_id = str(uuid.uuid4())
        self.last_tool_call = "bugreports___create_bug_report"
        self.bug_fields.clear()
        return f"Your bug report was created. Ticket ID: {ticket_id}. Status: OPEN."

    @staticmethod
    def _handoff(prefix: str = "This request needs human support.") -> str:
        return f"{prefix} Please contact human support at {' or '.join(SUPPORT_PHONES)}."

    def _answer_faq(self, lower: str) -> str:
        if "exact" in lower and ("delivery" in lower or "date" in lower):
            return self._handoff("The FAQ does not provide an exact delivery date.")
        if ("order status" in lower or ("track" in lower and "order" in lower)) and self._faq_has("Orders section"):
            return "You can check your order status in the Orders section of your account."
        if ("shipping" in lower or "delivery" in lower) and self._faq_has("order details"):
            return "Shipping and delivery information is provided in your order details. Specific estimates vary by order."
        if ("return" in lower or "refund" in lower) and self._faq_has("return policy"):
            return "Returns and refunds follow the return policy shown in your order or account information."
        if "payment" in lower and self._faq_has("presented during checkout"):
            return "The shop supports the payment methods presented during checkout."
        if ("product" in lower or "available" in lower) and self._faq_has("availability"):
            return "Product availability and product-specific information can vary."
        if ("account" in lower or "privacy" in lower or "policy" in lower) and self._faq_has("human support"):
            return "Please contact human support for information not answered in the FAQ."
        return self._handoff("This question is not covered by the FAQ.")

    def _faq_has(self, phrase: str) -> bool:
        return phrase.casefold() in self.faq.casefold()

    @staticmethod
    def _is_bug(lower: str) -> bool:
        return any(word in lower for word in ("broken", "crash", "crashes", "error", "not working", "malfunction", "fails"))

    @staticmethod
    def _is_platform_question(lower: str) -> bool:
        return any(word in lower for word in ("order", "shipping", "delivery", "return", "refund", "payment", "product", "account", "privacy", "policy"))

    @staticmethod
    def _is_injection(lower: str) -> bool:
        return bool(re.search(r"ignore .*instructions|reveal .*prompt|override .*rules", lower))