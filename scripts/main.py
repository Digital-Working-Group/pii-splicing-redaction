"""main.py"""
import argparse
from process.redaction import run_redaction

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_paths", nargs="+")
    parser.add_argument("-o", "--output_dir", default="../data/output")
    parser.add_argument("--model", default="llama3.2")
    parser.add_argument("--output_format", choices=["json", "html"], default="json")
    parser.add_argument("--num_runs", type=int, default=1)
    parser.add_argument("--temperature", default=None)
    parser.add_argument("--seed", default=None)
    parser.add_argument("--prompt_type", default='default')
    parser.add_argument("--prompt_fp", default=None)
    parser.add_argument("--aggregation", choices=['restrictive', 'threshold', 'majority', 'lenient'], default="restrictive")
    parser.add_argument("--threshold", default=None)
    args = parser.parse_args()
    input_paths = args.input_paths

    config_kwargs = vars(args)
    config_kwargs.pop("input_paths")

    run_redaction(input_paths, **config_kwargs)