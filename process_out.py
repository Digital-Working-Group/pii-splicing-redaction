"""process_out.py"""
import json
from pathlib import Path
from dataclasses import asdict
from typing import TextIO
from reports import generate_html_report
import llm
import pii_identification
from redaction import redact_text

def llm_message_out(output_file: TextIO, llm_raw_response: str):
    """Outputs raw llm message contents"""
    base_dir = Path(output_file.name).parent
    file_name = f'{Path(output_file.name).stem}.json'
    response_json = json.loads(llm_raw_response)
    model = response_json['model']
    output_dir = base_dir / model
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    with open(Path(output_dir) / file_name, "w", encoding="utf-8") as output_file:
        json.dump(response_json, output_file, indent=4)

def process_file_json_out(input_file: TextIO, output_file: TextIO, model: str, options: dict):
    """Identify PII, redact, and output redaction to a JSON"""
    text = input_file.read()
    try:
        entities, raw_response = llm.identify_pii(text, model, options)
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
        llm_message_out(output_file, raw_response)

    json.dump(asdict(results), output_file, indent=4)

def process_file_html_out(input_file: TextIO, output_file: TextIO, model: str, options: dict):
    """Identify PII, redact, and output redaction to an HTML"""
    text = input_file.read()
    try:
        entities, raw_response = llm.identify_pii(text, model, options)
    except json.JSONDecodeError as e:
        print(e)
        html_output = str(e)
    else:
        html_output = generate_html_report(text, [e.value for e in entities])
    output_file.write(html_output)


def process_path_json_out(input_path: Path, output_dir: Path, model: str, options: dict):
    """Creates output directory write JSON file."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    with open(input_path, encoding='utf-8') as input_file:
        with open(output_dir / input_path.with_suffix(".json").name, "w", encoding='utf-8') as out_file:
            process_file_json_out(input_file, out_file, model, options)

def process_path_html_out(input_path: Path, output_dir: Path, model: str, options: dict):
    """Creates output directory write HTML file."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    with open(input_path, encoding='utf-8') as input_file:
        with open(output_dir / input_path.with_suffix(".html").name, "w", encoding='utf-8') as out_file:
            process_file_html_out(input_file, out_file, model, options)