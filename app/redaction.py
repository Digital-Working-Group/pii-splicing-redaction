def redact_text(text: str, entities: "list[str]") -> str:
    for entity in entities:
        text = text.replace(entity, "<PII>")
    return text