"""process_out.py"""

import json
from pathlib import Path
from dataclasses import asdict
from typing import TextIO
from reports import generate_html_report
import llm
import pii_identification
from redaction import redact_text

def process_file_json_out(input_file: TextIO, output_file: TextIO, model: str):
    text = input_file.read()
    try:
        entities = llm.identify_pii(text, model, {})
    except json.JSONDecodeError as e:
        print(e)
        results = pii_identification.PIIResults(
            entities=[],
            source_text=text,
            redacted_text=text,
            errors=[str(e)],
        )
    else:
        redacted_text = redact_text(text, [entity.value for entity in entities])
        results = pii_identification.PIIResults(
            entities=entities,
            source_text=text,
            redacted_text=redacted_text,
        )

    json.dump(asdict(results), output_file, indent=4)

def process_file_html_out(input_file: TextIO, output_file: TextIO, model: str):
    text = input_file.read()
    try:
        entities = llm.identify_pii(text, model, {})
    except json.JSONDecodeError as e:
        print(e)
        html_output = str(e)
    else:
        html_output = generate_html_report(text, [e.value for e in entities])
    output_file.write(html_output)


def process_path_json_out(input_path: Path, output_dir: Path, model: str):
    with open(input_path) as input_file:
        with open(output_dir / input_path.with_suffix(".json").name, "w", encoding='utf-8') as out_file:
            process_file_json_out(input_file, out_file, model)

def process_path_html_out(input_path: Path, output_dir: Path, model: str):
    with open(input_path) as input_file:
        with open(output_dir / input_path.with_suffix(".html").name, "w", encoding='utf-8') as out_file:
            process_file_html_out(input_file, out_file, model)