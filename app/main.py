"""main.py"""

import argparse
from pathlib import Path
import sys
from process_out import process_file_html_out, process_file_json_out, process_path_html_out, process_path_json_out

def run_redaction(input_paths: "list[str]", output_dir: str, model: str, output_format: str, temperature: float, seed: int):
    options = {}
    if temperature is not None:
        options['temperature'] = float(temperature)
    if seed is not None:
        options['seed'] = int(seed)
    output_dir_path = Path(output_dir)
    if args.input_paths[0] == "-":
        input_file = sys.stdin

        if output_format == "html":
            with open(Path(output_dir) / "stdin.html", "w") as output_file:
                process_file_html_out(input_file, output_file, model, options)
        else:
            with open(Path(output_dir) / "stdin.json", "w") as output_file:
                process_file_json_out(input_file, output_file, model, options)
    else:
        for input_path in args.input_paths:
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_paths", nargs="+")
    parser.add_argument("-o", "--output_dir", default="/data/output")
    parser.add_argument("--output_format", choices=["json", "html"], default="json")
    parser.add_argument("--model", default="llama3.2")
    parser.add_argument("--temperature", default=None)
    parser.add_argument("--seed", default=None)
    args = parser.parse_args()

    run_redaction(args.input_paths, args.output_dir, args.model, args.output_format, args.temperature, args.seed)