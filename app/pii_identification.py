import dataclasses

@dataclasses.dataclass
class Entity:
    type: str
    value: str

@dataclasses.dataclass
class PIIResults:
    entities: "list[Entity]"
    source_text: str
    redacted_text: str
    errors: "list[str]" = dataclasses.field(default_factory=list)