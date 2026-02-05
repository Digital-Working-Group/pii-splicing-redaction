"""
sample_run.py
example of running run_redaction() from app.redact_pii
"""
from redact_pii import run_redaction

def main():
    """
    main entrypoint
    """
    options = {"num_runs": 4, }
    kwargs = {"output_dir": "./sample_redaction/sample_output", "output_format": "json", "model": "llama3.2",
              "num_runs": 4, "aggregation": "majority"}
    run_redaction(["./sample_redaction/sample_input"], **kwargs)
    kwargs = {"output_dir": "./sample_redaction/sample_output", "output_format": "html", "model": "llama3.2",
              "num_runs": 4, "aggregation": "majority"}
    run_redaction(["./sample_redaction/sample_input"], **kwargs)

if __name__ == '__main__':
    main()
