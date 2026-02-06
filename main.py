"""main.py"""
import argparse
# from pathlib import Path
# from process_out import process_input_path
# from typing import Optional
from redaction_config import RedactionConfig
from redaction import run_redaction

# def run_redaction(input_paths: "list[str]", output_dir: str, model: str,
#         output_format: str, num_runs: int, temperature: float, seed: int, prompt_type: str,
#         prompt_fp: Optional[str] = None): 
#     """Pass through arguments to process input files, create redacted output files."""
#     options = {}
#     if temperature is not None:
#         options['temperature'] = float(temperature)
#     if seed is not None:
#         options['seed'] = int(seed)
#     if prompt_fp is not None:
#         options['prompt_fp'] = str(prompt_fp)
#     options['num_runs'] = int(num_runs)
#     options['prompt_type'] = str(prompt_type)
#     output_dir_path = Path(output_dir)

#     for input_path in input_paths:
#         process_input_path(input_path, output_format, output_dir_path, model, options)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_paths", nargs="+")
    parser.add_argument("-o", "--output_dir", default="/data/output")
    parser.add_argument("--model", default="llama3.2")
    parser.add_argument("--output_format", choices=["json", "html"], default="json")
    parser.add_argument("--num_runs", type=int, default=1)
    parser.add_argument("--temperature", default=None)
    parser.add_argument("--seed", default=None)
    parser.add_argument("--prompt_type", default='default')
    parser.add_argument("--prompt_fp", default=None)
    parser.add_argument("--aggregation", choices=[], default=None)
    parser.add_argument("--threshold", default=None)
    args = parser.parse_args()
    input_paths = args.input_paths

    config_kwargs = vars(args)
    config_kwargs.pop("input_paths")

    config = RedactionConfig(**config_kwargs)
    run_redaction(input_paths, **config)