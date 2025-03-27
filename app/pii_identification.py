import dataclasses

@dataclasses.dataclass
class Entity:
    type: str
    value: str
    # start: int
    # end: int

@dataclasses.dataclass
class PIIResults:
    entities: "list[Entity]"
    source_text: str
    redacted_text: str