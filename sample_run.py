"""
sample_run.py
example of running run_redaction() from app.redact_pii
"""
from process.redaction import run_redaction
from process.aggregate import run_aggregation

def main():
    """
    main entrypoint
    """
    ## Run aggregation redaction on unprocessed files
    for prompt in ['default', 'one_shot', 'few_shot']:
        ## Run aggregation redaction on unprocessed files
        kwargs = {"output_dir": "./sample_redaction/sample_output", "output_format": "json", "model": "llama3.2", "prompt_type": prompt,
                    "num_runs": 4, "aggregation": "majority"}
        run_redaction(["./sample_redaction/sample_input"], **kwargs)
        kwargs = {"output_dir": "./sample_redaction/sample_output", "output_format": "html", "model": "llama3.2", "prompt_type": prompt,
                    "num_runs": 4, "aggregation": "majority"}
        run_redaction(["./sample_redaction/sample_input"], **kwargs)

        ## Run aggregation redaction on previously processed files
        run_aggregation("json", f"./sample_redaction/sample_output/llama3.2/{prompt}", "lenient", None)
        run_aggregation("html", f"./sample_redaction/sample_output/llama3.2/{prompt}", "lenient", None)
        run_aggregation("json", f"./sample_redaction/sample_output/llama3.2/{prompt}", "restrictive", None)
        run_aggregation("html", f"./sample_redaction/sample_output/llama3.2/{prompt}", "restrictive", None)
        run_aggregation("json", f"./sample_redaction/sample_output/llama3.2/{prompt}", "threshold", 0.75)
        run_aggregation("html", f"./sample_redaction/sample_output/llama3.2/{prompt}", "threshold", 0.75)

if __name__ == '__main__':
    main()
