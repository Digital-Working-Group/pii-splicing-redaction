"""
sample_run.py
example of running run_redaction() from app.redact_pii
"""
from redact_pii import run_redaction

def main():
    """
    main entrypoint
    """
    kwargs = {"output_dir": "./sample_redaction/sample_output", "output_format": "json", "model": "llama3.2"}
    run_redaction(["./sample_redaction/sample_input"], **kwargs)
    kwargs = {"output_dir": "./sample_redaction/sample_output", "output_format": "html", "model": "llama3.2"}
    run_redaction(["./sample_redaction/sample_input"], **kwargs)

if __name__ == '__main__':
    main()
