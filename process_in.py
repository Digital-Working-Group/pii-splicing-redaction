"""process_in.py"""
from pathlib import Path
import re
import json
from pii_identification import Entity
from bs4 import BeautifulSoup as bsoup

def process_previously_generated(input_dir, output_format):
    """Collect multiple previous runs on the same file"""
    files = []
    for item in input_dir.iterdir():
        if item.is_file():
            if output_format == "json" and re.match('.*\d+\.json$', item.name) \
            or output_format == "html" and re.match('.*\d+\.html$', item.name):
                files.append(item)
    return files

def get_html_text(file):
    """ Collect the original text from an html file"""
    print(f"openning file {file}")
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
    soup = bsoup(content, 'html.parser')
    print(soup)
    text = soup.body.get_text()
    ## removing span tags
    text = text.replace('<span class="r1">', '')
    text = text.replace('</span>', '')
    print(text)
    return text

def get_json_text(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    body = data['source_text']
    return body

def collect_json_entities(files):
    """Collects the entities outputted as JSON files"""
    all_entities = []
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        for entity in data['entities']:
            all_entities.append(Entity(**entity))
        # all_entities.extend(data['entities'])
    return all_entities

def collect_html(files):
    """ Collect the results from individual runs outputted as HTML files"""
    all_pii_list = []
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
    return all_pii_list

## Not currently using this one, but could switch to it
def collect_raw_response(files):
    """ Collect the results from individual runs outputted as JSON files"""
    pii_words = []
    pii_labels_dict = {}
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        try:
            ## This gets only one of each instance per entity
            pii_words.extend(set(item["value"] for item in data['entities']))
            ## The get what each item 
            pii_labels_dict.update({item.value: item.type for item in data['entities']})
        except json.JSONDecodeError as err:
            print(err)
    return pii_words, pii_labels_dict

def get_data_from_result(output_format, files):
    """
    Get the text and entities associated with a previous output file
    """
    if output_format == "html":
        text = get_html_text(files[0])
        entities = collect_html(files)
    elif output_format == "json":
        text = get_json_text(files[0])
        entities = collect_json_entities(files)
    else:
        raise ValueError(f'Unsupported output format entered {output_format}.')
    return text, entities
