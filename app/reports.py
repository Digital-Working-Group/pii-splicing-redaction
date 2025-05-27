"""reports.py"""
import os
from typing import TextIO

def generate_html_report(text: str, predicted_entities: "list[str]"):
    from rich.table import Table
    from rich.console import Console

    devnull = "nul" if os.name == "nt" else "/dev/null"

    with open(devnull, "w") as f:
        console = Console(record=True, file=f)
        
        # First highlight all AI found values in purple
        for value in predicted_entities:
            # Skip empty strings. Otherwise, every gap betwen characters will be filled in the .replace
            if not value:
                continue
            text = text.replace(value, f"[purple]{value}[/purple]")
                    
        # Remove blank lines from highlighted text
        highlighted_text = '\n'.join(line for line in text.split('\n') if line.strip())
        
        console.print(highlighted_text)

        return console.export_html()
