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
    as_path = Path(output_file.name)
    base_dir = as_path.parent
    ext = as_path.suffix.replace(".", "-")
    file_name = f'{as_path.stem}{ext}.json'
    response_json = json.loads(llm_raw_response)
    output_dir = base_dir / 'llm_raw_response'
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    with open(Path(output_dir) / file_name, "w", encoding="utf-8") as json_out:
        json.dump(response_json, json_out, indent=4)

def get_text_and_response(input_file, model, options):
    """
    get the text from the input_file, get response from the llm model
    """
    text = input_file.read()
    response = llm.identify_pii(text, model, options)
    return text, response

def process_file_json_out(input_file: TextIO, output_file: TextIO, model: str, options: dict):
    """Identify PII, redact, and output redaction to a JSON"""
    text, response = get_text_and_response(input_file, model, options)
    llm_message_out(output_file, response.model_dump_json())
    try:
        entities = llm.parse_model_output(response.message.content)
    except json.JSONDecodeError as err:
        print(err)
        results = pii_identification.PIIResults(
            entities=[],
            source_text=text,
            redacted_text=text,
            errors=[str(err)],
        )
    else:
        redacted_text = redact_text(text, [entity.value for entity in entities])
        results = pii_identification.PIIResults(
            entities=entities,
            source_text=text,
            redacted_text=redacted_text,
        )

    json.dump(asdict(results), output_file, indent=4)

def process_file_html_out(input_file: TextIO, output_file: TextIO, model: str, options: dict):
    """Identify PII, redact, and output redaction to an HTML"""
    text, response = get_text_and_response(input_file, model, options)
    llm_message_out(output_file, response.model_dump_json())
    try:
        entities = llm.parse_model_output(response.message.content)
    except json.JSONDecodeError as err:
        print(err)
        html_output = str(err)
    else:
        html_output = generate_html_report(text, [e.value for e in entities])
    output_file.write(html_output)

def process_path_out(input_path: Path, output_dir: Path, model: str, options: dict, output_format: str):
    """Creates output directory write JSON or HTML file."""
    output_dir = output_dir / model
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    out_filepath = output_dir / input_path.with_suffix(f'.{output_format}').name
    with open(input_path, encoding='utf-8') as input_file, open(out_filepath, "w", encoding='utf-8') as out_file:
        if output_format == 'html':
            process_file_html_out(input_file, out_file, model, options)
        else:
            process_file_json_out(input_file, out_file, model, options)

def process_input_path(input_path, output_format, output_dir_path, model, options):
    """
    process an file (input_path) or directory of text files
    """
    input_path = Path(input_path)
    if input_path.is_dir():
        for file in input_path.glob("*.txt"):
            process_path_out(file, output_dir_path, model, options, output_format)
    else:
        process_path_out(input_path, output_dir_path, model, options, output_format)
