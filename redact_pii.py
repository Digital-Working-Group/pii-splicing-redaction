"""redact_pii.py"""

from pathlib import Path
import sys
from process_out import process_file_html_out, process_file_json_out, process_path_html_out, process_path_json_out

def run_redaction(input_paths, **kwargs):
    """Pass through arguments to process input files, create redacted output files."""
    output_dir = kwargs.get("output_dir", "./sample_redaction/sample_output")
    output_format = kwargs.get("output_format", "json")
    model = kwargs.get("model", "llama3.2")
    options = {}
    temperature = kwargs.get("temperature", None)
    seed = kwargs.get("seed", None)
    if temperature is not None:
        options['temperature'] = float(temperature)
    if seed is not None:
        options['seed'] = int(seed)
    options = kwargs.get("options", {})

    output_dir_path = Path(output_dir)
    if input_paths[0] == "-":
        input_file = sys.stdin

        if output_format == "html":
            with open(Path(output_dir) / "stdin.html", "w", encoding="utf-8") as output_file:
                process_file_html_out(input_file, output_file, model, options)
        else:
            with open(Path(output_dir) / "stdin.json", "w", encoding="utf-8") as output_file:
                process_file_json_out(input_file, output_file, model, options)
    else:
        for input_path in input_paths:
            input_path = Path(input_path)
            process_func = process_path_html_out if output_format == "html" else process_path_json_out
            if input_path.is_dir():
                for file in input_path.glob("*.txt"):
                    process_func(file, output_dir_path, model, options)
            else:
                process_func(input_path, output_dir_path, model, options)
