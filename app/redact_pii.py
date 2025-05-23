"""redact_pii.py"""

import argparse
import json
from pathlib import Path
from dataclasses import asdict
import sys
from typing import TextIO
from reports import generate_html_report
import llm
import pii_identification
from redaction import redact_text
from process_out import process_file_html_out, process_file_json_out, process_path_html_out, process_path_json_out

def run_redaction(input_paths, **kwargs):
    output_dir = kwargs.get("output_dir", "./sample_redaction/sample_output")
    output_format = kwargs.get("output_format", "json")
    model = kwargs.get("model", "llama3.2")
    options = {}
    temperature = kwargs.get("temperature", None)
    seed = kwargs.get("seed", None)
    if temperature is not None:
        options
    options = kwargs.get("options", {})

    output_dir_path = Path(output_dir)
    if input_paths[0] == "-":
        input_file = sys.stdin

        if output_format == "html":
            with open(Path(output_dir) / "stdin.html", "w") as output_file:
                process_file_html_out(input_file, output_file, model, options)
        else:
            with open(Path(output_dir) / "stdin.json", "w") as output_file:
                process_file_json_out(input_file, output_file, model, options)
    else:
        for input_path in input_paths:
            input_path = Path(input_path)
            if input_path.is_dir():
                for file in input_path.glob("*.txt"):
                    if output_format == "html":
                        process_path_html_out(file, output_dir_path, model, options)
                    else:
                        process_path_json_out(file, output_dir_path, model, options)
            else:
                if output_format == "html":
                    process_path_html_out(input_path, output_dir_path, model, options)
                else:
                    process_path_json_out(input_path, output_dir_path, model, options)

def main():
    ## Sample

    kwargs = {"output_format": "html",
              "seed": 30}

    run_redaction(["./sample_redaction/sample_input/test.txt"])
    run_redaction(["./sample_redaction/sample_input/test.txt"], **kwargs)

if __name__ == "__main__":
    main()