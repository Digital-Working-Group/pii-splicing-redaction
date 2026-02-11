"""
aggreate.py
functions to perform aggregation on multiple runs
"""
from bs4 import BeautifulSoup as bsoup 
from pathlib import Path
from collections import Counter
from dataclasses import asdict
from reports import generate_html_report, generate_json_report
from process_in import get_data_from_result, process_previously_generated, collect_html, collect_json
import json
import os
import re

def run_aggregation(output_format, output_dir, aggregation, threshold):
    """
    aggregate on data that has already been created
    """
    output_dir = Path(output_dir)
    for subdir in output_dir.iterdir():
        if subdir.is_dir():
            files = process_previously_generated(subdir)
            ## TODO: remove
            print(f'Files found {files}')
            if len(files) > 1:
                file_stem = files[0].stem.split("_")[0]
                agg_out_filepath = output_dir / f'{file_stem}_{aggregation}.{output_format}'
                text, total_entities = get_data_from_result(output_format, files)
                redact_items = aggregate_runs(output_format, files, aggregation, threshold)
                process_aggregate_result(agg_out_filepath, output_format, text, redact_items, total_entities)
            else:
                print(f'Not enough files to perform aggregation. Found {len(files)} and need at least 2.')
        else:
            print(f'Skipping {subdir}, not a directory.')

def process_aggregate_result(output_filepath, output_format, text, redact_items, total_entities):
    """Process and write aggregate result"""
    with open(output_filepath, "w", encoding='utf-8') as out_file:
        if output_format == "html":
            html_output = generate_html_report(text, [item for item in redact_items])
            out_file.write(html_output)
        else:
            print(total_entities)
            json_output = generate_json_report(text, total_entities, redact_items)
            json.dump(asdict(json_output), out_file, indent=4)

def filter_pii(threshold, total_runs, counts_dict):
    """Calculates the percentage of runs that count a word as PII and compares to the redaction threshold"""
    redact_list = []
    for pii_text, count in counts_dict.items():
        if count/total_runs >= threshold:
            print(f'greater than threshold!\nThreshold: {threshold} Value: {count/total_runs}\n{pii_text} should be redacted.')
            redact_list.append(pii_text)
    return redact_list

def aggregate_runs(output_format, files, aggregation, threshold=0):
    """Aggregate the results from individual runs"""

    aggregation_thresholds = {
        "threshold": threshold,
        "restrictive": 0,
        "lenient": 1,
        "majority": 0.5,
    }
    if output_format == 'html':
        pii_list = collect_html(files)
    elif output_format == 'json':
        pii_list = collect_json(files)
    else:
        raise ValueError(f'Unsupported output format entered {output_format}.')
    pii_counts = Counter(pii_list)
    agg_threshold = aggregation_thresholds.get(aggregation, 0)
    return filter_pii(agg_threshold, len(files), pii_counts)

def test_html(filepath):
    collect_html([filepath])

def test_json(filepath):
    collect_json([filepath])

if __name__ == '__main__':
    # test_html('sample_redaction/sample_output/llama3.2/test.html')
    test_json('sample_redaction/sample_output/llama3.2/test.json')