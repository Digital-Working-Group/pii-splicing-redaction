"""process_out.py"""
import json
from pathlib import Path
from dataclasses import asdict
from typing import TextIO
from reports import generate_html_report, generate_json_report
import llm
import pii_identification
from aggregate import aggregate_runs, process_aggregate_result

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

def get_entities(response: dict):
    """
    Parse the LLM output for entities to redact
    Returns entities and the error message (if error), else None
    """
    try:
        entities = llm.parse_model_output(response.message.content)
        return entities, None
    except json.JSONDecodeError as err:
        print(err)
        entities = []
        return entities, err

def process_file_json_out(text: str, entities: list, error_msg: str, output_file: TextIO):
    """Output redaction to a JSON"""
    if error_msg:
        results = pii_identification.PIIResults(
            entities=[],
            source_text=text,
            redacted_text=text,
            errors=[str(error_msg)],
        )
    else:
        results = generate_json_report(text, entities)

    json.dump(asdict(results), output_file, indent=4)

def process_file_html_out(text: str, entities: list, error_msg: str, output_file: TextIO):
    """Output redaction to an HTML"""
    if error_msg:
        html_output = str(error_msg)
    else:
        html_output = generate_html_report(text, [e.value for e in entities])
    output_file.write(html_output)

def process_path_out(input_path: Path, output_dir: Path, model: str, options: dict, output_format: str):
    """Creates output directory write JSON or HTML file."""
    files_created = []
    aggregation = options.get("aggregation", "restrictive")
    threshold = options.get("threshold", 0)
    file_stem = f'{input_path.stem}'
    output_dir = output_dir / model / file_stem
    total_entities = []
    for i in range(options.get('num_runs')):
        ## Create output directory
        if options.get('num_runs') == 1:
            out_filepath = output_dir / f'{file_stem}.{output_format}'
        else:
            out_filepath = output_dir / f'{file_stem}_{i}.{output_format}'
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        with open(input_path, encoding='utf-8') as input_file, open(out_filepath, "w", encoding='utf-8') as out_file:
            ## Get LLM response are parse for entities
            text, response = get_text_and_response(input_file, model, options)
            llm_message_out(out_file, response.model_dump_json())
            entities, error = get_entities(response)
            total_entities.extend(entities)
            ## Output files
            if output_format == 'html':
                process_file_html_out(text, entities, error, out_file)
            else:
                process_file_json_out(text, entities, error, out_file)
        ## Append to list
        files_created.append(out_filepath)
    if options.get('num_runs') > 1:
        redact_items = aggregate_runs(output_format, files_created, aggregation, threshold)
        agg_out_filepath = output_dir / f'{file_stem}_{aggregation}.{output_format}'
        process_aggregate_result(agg_out_filepath, output_format, text, redact_items, total_entities)

def process_input_path(input_path, redaction_config):
    """
    process an file (input_path) or directory of text files
    """
    input_path = Path(input_path)
    files_created = []
    if input_path.is_dir():
        for file in input_path.glob("*.txt"):
            files_created.append(process_path_out(file, redaction_config.output_dir_path, redaction_config.model, 
                                                  redaction_config.options, redaction_config.output_format))
    else:
        files_created.append(process_path_out(input_path, redaction_config.output_dir_path, redaction_config.model, 
                                              redaction_config.options, redaction_config.output_format))