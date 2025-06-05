"""redact_pii.py"""

from pathlib import Path
from process_out import process_input_path

def run_redaction(input_paths, **kwargs):
    """Pass through arguments to process input files, create redacted output files."""
    output_dir = kwargs.get("output_dir", "./sample_redaction/sample_output")
    output_format = kwargs.get("output_format", "json")
    model = kwargs.get("model", "llama3.2")
    options = kwargs.get("options", {})
    temperature = kwargs.get("temperature", None)
    seed = kwargs.get("seed", None)
    if temperature is not None:
        options['temperature'] = float(temperature)
    if seed is not None:
        options['seed'] = int(seed)
    output_dir_path = Path(output_dir)
    for input_path in input_paths:
        process_input_path(input_path, output_format, output_dir_path, model, options)
