"""reports.py"""
import os
from rich.console import Console
from process.redact_pii import redact_text
import config.pii_identification as pii_identification

def generate_html_report(text: str, predicted_entities: "list[str]"):
    """Format HTML output summary"""
    devnull = "nul" if os.name == "nt" else "/dev/null"
    with open(devnull, "w", encoding="utf-8") as f:
        console = Console(record=True, file=f)
        # First highlight all AI found values in purple
        for value in predicted_entities:
            # Skip empty strings.
            # Otherwise, every gap between characters will be filled in the .replace
            if not value:
                continue
            text = text.replace(value, f"[purple]{value}[/purple]")
        # Remove blank lines from highlighted text
        highlighted_text = '\n'.join(line for line in text.split('\n') if line.strip())
        console.print(highlighted_text, highlight=False)
        return console.export_html()

def generate_json_report(text: str, entities: list, redact_list=None):
    """Format JSON Summary
    If a redaction list exists, edit the entities to only contain items
    from the redact list"""
    seen = set()
    if redact_list != None:
        ## Add one copy of each entitiy to redact to entities
        entities = [e for e in entities 
                    if e.value in redact_list and not(e.value in seen or seen.add(e.value))]
    redacted_text = redact_text(text, [e.value for e in entities])
    return pii_identification.PIIResults(
        entities=entities,
        source_text=text,
        redacted_text=redacted_text,
    )
