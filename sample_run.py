"""
sample_run.py
example of running run_redaction() from app.redact_pii
"""
from redaction import run_redaction
from aggregate import run_aggregation

def main():
    """
    main entrypoint
    """
    ## Run aggregation redaction on unprocessed files
    kwargs = {"output_dir": "./sample_redaction/sample_output", "output_format": "json", "model": "llama3.2", "prompt_type": "one_shot",
              "num_runs": 4, "aggregation": "majority"}
    run_redaction(["./sample_redaction/sample_input"], **kwargs)
    kwargs = {"output_dir": "./sample_redaction/sample_output", "output_format": "html", "model": "llama3.2",
              "num_runs": 4, "aggregation": "majority"}
    run_redaction(["./sample_redaction/sample_input"], **kwargs)
    ## Run aggregation redaction on previously processed files
    run_aggregation("json", "./sample_redaction/sample_output/llama3.2", "lenient", None)
    run_aggregation("html", "./sample_redaction/sample_output/llama3.2", "lenient", None)

if __name__ == '__main__':
    main()
