"""redaction.py"""

def redact_text(text: str, entities: "list[str]") -> str:
    """Redact text based on entities identified"""
    for entity in entities:
        text = text.replace(entity, "<PII>")
    return text