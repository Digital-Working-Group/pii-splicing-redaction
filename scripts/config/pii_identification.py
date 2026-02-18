"""pii_identification.py"""
import dataclasses

@dataclasses.dataclass
class Entity:
    """PII type and value"""
    type: str
    value: str

@dataclasses.dataclass
class PIIResults:
    """PII results"""
    entities: "list[Entity]"
    source_text: str
    redacted_text: str
    errors: "list[str]" = dataclasses.field(default_factory=list)
