import argparse
import json
from pathlib import Path
from dataclasses import asdict
import sys
from typing import TextIO

import models
import pii_identification
from redaction import redact_text

def process_file(input_file: TextIO, output_file: TextIO, model: str):
    text = input_file.read()
    entities = models.identify_pii(text, model, {})
    redacted_text = redact_text(text, [entity.value for entity in entities])

    results = pii_identification.PIIResults(
        entities=entities,
        source_text=text,
        redacted_text=redacted_text
    )

    json.dump(asdict(results), output_file)

def process_path(input_path: Path, output_dir: Path, model: str):
    with open(input_path) as input_file:
        with open(output_dir / input_path.with_suffix(".json").name, "w") as out_file:
            process_file(input_file, out_file, model)


def main(input_paths: "list[str]", output_dir: str, model: str, write_html: bool):
    output_dir_path = Path(output_dir)
    if args.input_paths[0] == "-":
        if len(args.input_paths) > 1:
            raise ValueError("Only one input can be provided when using stdin")
        input_file = sys.stdin
        with open(Path(output_dir) / "stdin.json", "w") as output_file:
            process_file(input_file, output_file, model)
    else:
        for input_path in args.input_paths:
            input_path = Path(input_path)
            if input_path.is_dir():
                for file in input_path.glob("*.txt"):
                    process_path(file, output_dir_path, model)
            else:
                process_path(input_path, output_dir_path, model)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_paths", nargs="+")
    parser.add_argument("-o", "--output_dir", default="/data/output")
    parser.add_argument("--write_html", action="store_true")
    parser.add_argument("--model", default="llama3.2")
    args = parser.parse_args()

    main(args.input_paths, args.output_dir, args.model, args.write_html)