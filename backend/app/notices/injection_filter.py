SUSPICIOUS_PATTERNS = [
    "ignore previous instructions",
    "ignoriere vorherige anweisungen",
    "system prompt",
    "developer message",
    "du bist jetzt",
    "antworte ohne quellen",
    "vergiss alle regeln",
]


def sanitize_untrusted_document_text(text: str) -> tuple[str, list[str]]:
    findings: list[str] = []
    lower = text.lower()
    for pattern in SUSPICIOUS_PATTERNS:
        if pattern in lower:
            findings.append(pattern)
    return text, findings
