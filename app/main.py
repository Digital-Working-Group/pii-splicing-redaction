import argparse
import json
from pathlib import Path
from dataclasses import asdict
import sys
from typing import TextIO

from app.reports import generate_html_report
import models
import pii_identification
from redaction import redact_text

def process_file_json_out(input_file: TextIO, output_file: TextIO, model: str):
    text = input_file.read()
    entities = models.identify_pii(text, model, {})
    redacted_text = redact_text(text, [entity.value for entity in entities])

    results = pii_identification.PIIResults(
        entities=entities,
        source_text=text,
        redacted_text=redacted_text
    )

    json.dump(asdict(results), output_file)

def process_file_html_out(input_file: TextIO, output_file: TextIO, model: str):
    text = input_file.read()
    entities = models.identify_pii(text, model, {})

    generate_html_report(text, [e.value for e in entities], output_file)


def process_path_json_out(input_path: Path, output_dir: Path, model: str):
    with open(input_path) as input_file:
        with open(output_dir / input_path.with_suffix(".json").name, "w") as out_file:
            process_file_json_out(input_file, out_file, model)

def process_path_html_out(input_path: Path, output_dir: Path, model: str):
    with open(input_path) as input_file:
        with open(output_dir / input_path.with_suffix(".json").name, "w") as out_file:
            process_file_html_out(input_file, out_file, model)

def main(input_paths: "list[str]", output_dir: str, model: str, output_format: str):
    output_dir_path = Path(output_dir)
    if args.input_paths[0] == "-":
        input_file = sys.stdin

        if output_format == "html":
            with open(Path(output_dir) / "stdin.html", "w") as output_file:
                process_file_html_out(input_file, output_file, model)
        else:
            with open(Path(output_dir) / "stdin.json", "w") as output_file:
                process_file_json_out(input_file, output_file, model)
    else:
        for input_path in args.input_paths:
            input_path = Path(input_path)
            if input_path.is_dir():
                for file in input_path.glob("*.txt"):
                    if output_format == "html":
                        process_path_html_out(file, output_dir_path, model)
                    else:
                        process_path_json_out(file, output_dir_path, model)
            else:
                if output_format == "html":
                    process_path_html_out(input_path, output_dir_path, model)
                else:
                    process_path_json_out(input_path, output_dir_path, model)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_paths", nargs="+")
    parser.add_argument("-o", "--output_dir", default="/data/output")
    parser.add_argument("--output_format", choices=["json", "html"], default="json")
    parser.add_argument("--model", default="llama3.2")
    args = parser.parse_args()

    main(args.input_paths, args.output_dir, args.model, args.output_format)