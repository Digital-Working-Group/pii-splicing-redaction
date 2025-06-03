"""main.py"""
import argparse
from pathlib import Path
from process_out import process_input_path

def run_redaction(input_paths: "list[str]", output_dir: str, model: str,
        output_format: str, temperature: float, seed: int):
    """Pass through arguments to process input files, create redacted output files."""
    options = {}
    if temperature is not None:
        options['temperature'] = float(temperature)
    if seed is not None:
        options['seed'] = int(seed)
    output_dir_path = Path(output_dir)
    for input_path in input_paths:
        process_input_path(input_path, output_format, output_dir_path, model, options)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_paths", nargs="+")
    parser.add_argument("-o", "--output_dir", default="/data/output")
    parser.add_argument("--model", default="llama3.2")
    parser.add_argument("--output_format", choices=["json", "html"], default="json")
    parser.add_argument("--temperature", default=None)
    parser.add_argument("--seed", default=None)
    args = parser.parse_args()
    run_redaction(args.input_paths, args.output_dir, args.model, args.output_format,
        args.temperature, args.seed)
