import re
from src.utils.exceptions.custom_exceptions import PIIDetectionError

API_KEY_PATTERN = re.compile(r"sk-[a-zA-Z0-9]{32,}")
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
CREDIT_CARD_PATTERN = re.compile(r"\b(?:\d[ -]?){13,19}\b")
IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
PHONE_PATTERN = re.compile(r"(?:\+?\d{1,3}[-.\s]?)?\d{10}\b")


def apply_pii_guardrails(text: str) -> str:
    print(f"[PII GUARD] Original user input: {text}")

    if API_KEY_PATTERN.search(text):
        raise PIIDetectionError("API key detected in input.")

    sanitized = text
    if EMAIL_PATTERN.search(sanitized):
        sanitized = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", sanitized)
    if CREDIT_CARD_PATTERN.search(sanitized):
        sanitized = CREDIT_CARD_PATTERN.sub("[REDACTED_CARD]", sanitized)
    if PHONE_PATTERN.search(sanitized):
        sanitized = PHONE_PATTERN.sub("[REDACTED_PHONE]", sanitized)
    if IP_PATTERN.search(sanitized):
        sanitized = IP_PATTERN.sub("[REDACTED_IP]", sanitized)

    if sanitized != text:
        print(f"[PII GUARD] Sanitized text: {sanitized}")
    else:
        print("[PII GUARD] No PII detected. Passing input unchanged.")

    return sanitized