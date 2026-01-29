"""main.py"""
import argparse
from pathlib import Path
from process_out import process_input_path

def run_redaction(input_paths: "list[str]", output_dir: str, model: str,
        output_format: str, num_runs: int, temperature: float, seed: int, custom_prompt: str,
        prompt_example: str, one_shot: bool): 
    """Pass through arguments to process input files, create redacted output files."""
    options = {}
    prompt_options = {}
    if temperature is not None:
        options['temperature'] = float(temperature)
    if seed is not None:
        options['seed'] = int(seed)
    output_dir_path = Path(output_dir)
    if custom_prompt is not None:
        prompt_options['custom_prompt'] = custom_prompt
    if prompt_example is not None:
        prompt_options['prompt_example'] = prompt_example
    if one_shot:
        prompt_options['one_shot'] = one_shot
    for input_path in input_paths:
        for _ in range(num_runs):
            process_input_path(input_path, output_format, output_dir_path, model, options, prompt_options)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_paths", nargs="+")
    parser.add_argument("-o", "--output_dir", default="/data/output")
    parser.add_argument("--model", default="llama3.2")
    parser.add_argument("--output_format", choices=["json", "html"], default="json")
    parser.add_argument("--num_runs", type=int, default=1)
    parser.add_argument("--temperature", default=None)
    parser.add_argument("--seed", default=None)
    parser.add_argument("--custom_prompt", default=None)
    parser.add_argument('--prompt_example', default=None)
    parser.add_argument('--one_shot', action='store_true')
    args = parser.parse_args()
    run_redaction(args.input_paths, args.output_dir, args.model, args.output_format, args.num_runs,
        args.temperature, args.seed, args.custom_prompt, args.prompt_example, args.one_shot)