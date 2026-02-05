
## TODO: consider moving all of the aggregation functions to a separate file
from bs4 import BeautifulSoup as bsoup 
from collections import defaultdict, Counter
import json

def collect_html(files):
    """ Collect the results from individual runs outputted as HTML files"""
    all_pii_list = []
    ## build list of PII
    ## only add one of each entry per file
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        soup = bsoup(content, 'html.parser')
        spans = soup.find_all('span', class_='r1')
        pii_items = set([s.get_text(strip=True) for s in spans])
        all_pii_list.extend(pii_items)
    return all_pii_list


def collect_json(files):
    """ Collect the results from individual runs outputted as JSON files"""
    all_pii_list = []
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        pii_items = set(item["value"] for item in data['entities'])
        all_pii_list.extend(pii_items)
    print(all_pii_list)
    return all_pii_list

## TODO: Not currently using this one, but could switch to it
def collect_raw_json(files):
    """ Collect the results from individual runs outputted as JSON files"""
    all_pii = []
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
    pass

def filter_pii(threshold, total_runs, counts_dict):
    """Calculates the percentage of runs that count a word as PII and compares to the redaction threshold"""
    redact_list = []
    for pii_text, count in counts_dict.items():
        if count/total_runs >= threshold:
            print('greater than threshold! {pii_text} should be redacted.')
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
    else:
        pii_list = collect_json(files)
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