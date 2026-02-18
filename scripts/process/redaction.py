"""redaction.py"""
from process.process_out import process_input_path
from config.redaction_config import RedactionConfig

def run_redaction(input_paths, **kwargs):
    """Pass through arguments to process input files, create redacted output files."""
    config = RedactionConfig(**kwargs)

    for input_path in input_paths:
        process_input_path(input_path, config)
