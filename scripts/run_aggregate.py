"""
aggreate.py
functions to perform aggregation on multiple runs
"""
import argparse
from process.aggregate import run_aggregation

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output_dir", default="out/llama3.2")
    parser.add_argument("--output_format", choices=["json", "html"], default="json")
    parser.add_argument("--aggregation", choices=['restrictive', 'threshold', 'majority', 'lenient'], default="restrictive")
    parser.add_argument("--threshold", default=None)
    args = parser.parse_args()

    run_aggregation(args.output_format, args.output_dir, args.aggregation, args.threshold)