"""pii_masking_evaluate.py"""
from pathlib import Path
import json
import pprint
import re
import os
import sys
from datetime import datetime
import pandas as pd
from export_pii_masking_300k import load_hugging_face_dataset

def calc_summary_metrics(counts_dict):
    """
    calculate summary metrics
    """
    true_pos = counts_dict['total_true_positives']
    true_neg = counts_dict['total_true_negatives']
    false_pos = counts_dict['total_false_positives']
    false_neg = counts_dict['total_false_negatives']

    precision = true_pos / (true_pos + false_pos)
    recall = true_pos / (true_pos + false_neg)
    f1_score = (2 * precision * recall) / (precision + recall)

    precision = round(100 * precision, 1)
    recall = round(100 * recall, 1)
    f1_score = round(100 * f1_score, 1)
    summary = {
        "True Positives": true_pos,
        "True Negatives": true_neg,
        "False Positives": false_pos,
        "False Negatives": false_neg,
        "Precision": f'{precision}%',
        "Recall": f'{recall}%',
        "F1": f'{f1_score}%'
    }
    return summary

def write_summary_json(output_root, counts_dict, file_list, start_time, print_summary=True):
    """Write evaluation summary to a JSON file"""
    print(f'outroot is {output_root}')
    summary = calc_summary_metrics(counts_dict)
    summary.update({
        "Non matches": counts_dict['total_non_matches'],
        "Errors": counts_dict['error_count'],
        "Total files": counts_dict['total_files'],
        "Files": file_list,
        "Ran at": start_time.strftime("%Y-%m-%d %H:%M:%S")
    })

    if print_summary is True:
        pprint.pprint(summary)

    json_fp = os.path.join(output_root, f'summary_{start_time.strftime("%Y%m%d_%H%M%S")}.json')
    with open(json_fp, 'w', encoding='utf-8') as fp:
        json.dump(summary, fp, default=str, indent=4)

def write_summary_xlsx(output_root, summary_df, start_time):
    """Write evaluation summary to an excel file"""
    xlsx_fp = os.path.join(output_root, f'summary_{start_time.strftime("%Y%m%d_%H%M%S")}.xlsx')
    writer = pd.ExcelWriter(xlsx_fp, engine='xlsxwriter')
    summary_df.to_excel(writer, sheet_name='Summary', index=False)
    for group, data in summary_df.groupby(['filename']):
        tech_id = group[0]
        data.drop(labels='filename', axis=1, inplace=True)
        data.to_excel(writer, sheet_name=tech_id, index=False)
    writer.close()

def get_target_entities(privacy_mask):
    """
    get target entities from the privacy_mask
    """
    target_entities = set()
    for entity in privacy_mask:
        for word in re.split(r"[^a-zA-Z0-9]+", entity["value"]):
            target_entities.add(word.lower())
    return target_entities

def get_predicted_entities(entities, source_text_lower, counts_dict):
    """
    get predicted entities from entities
    if the word isn't in the source text, count it as a non-match
    """
    predicted_entities = set()
    for predicted_entity in entities:
        for word in re.split(r"[^a-zA-Z0-9]+", predicted_entity["value"]):
            print("Predicted word", word)
            word = word.lower()
            predicted_entities.add(word.lower())
            if word not in source_text_lower:
                counts_dict['total_non_matches'] += 1
    return predicted_entities

def classify_predictions(source_text_lower, predicted_entities, target_entities, counts_dict):
    """
    classify predicted entities as TP/FP/TN/FP
    """
    for word in re.split(r"[^a-zA-Z0-9]+", source_text_lower):
        is_predicted_pii = word in predicted_entities
        is_true_pii = word in target_entities
        status = ''
        if is_predicted_pii and is_true_pii:
            counts_dict['total_true_positives'] += 1
            status = "true_positives"
        elif is_predicted_pii and not is_true_pii:
            counts_dict['total_false_positives'] += 1
            status = "false_positives"
        elif not is_predicted_pii and is_true_pii:
            counts_dict['total_false_negatives'] += 1
            status = "false_negatives"
        else:
            counts_dict['total_true_negatives'] += 1
            status = "true_negatives"
        yield word, status


def init_data_structures():
    """
    initialize various data structures
    """
    file_list = []
    dataset = load_hugging_face_dataset()
    counts_dict = {
        'total_true_positives': 0,
        'total_false_positives': 0,
        'total_true_negatives': 0,
        'total_false_negatives': 0,
        'total_non_matches': 0,
        'error_count': 0,
        'total_files': 0
    }
    summary_df = pd.DataFrame(columns=['filename', 'predicted_word', 'status'])
    return file_list, dataset, counts_dict, summary_df

def write_output(file_list, counts_dict, start_time, summary_df):
    """write output files"""
    output_root = file_list[0].parent / 'summaries'
    output_root.mkdir(parents=True, exist_ok=True)
    filename_list = [f.name for f in file_list]
    # Write summaries
    write_summary_json(output_root, counts_dict, filename_list, start_time, print_summary=True)
    write_summary_xlsx(output_root, summary_df, start_time)

def process_pii_json(file, dataset, counts_dict, summary_df):
    """
    process_pii_json
    """
    with open(file, encoding='utf-8') as in_file:
        json_data = json.load(in_file)
    counts_dict['total_files'] += 1
    if json_data['errors'] != []:
        counts_dict['error_count'] += 1
        return None
    ds_row = dataset[int(file.name.split(".json")[0])]
    target_entities = get_target_entities(ds_row["privacy_mask"])
    source_text_lower = ds_row["source_text"].lower()
    predicted_entities = get_predicted_entities(json_data["entities"], source_text_lower,
        counts_dict)
    print(target_entities)
    print(ds_row["privacy_mask"])
    print(ds_row["source_text"])
    words_and_statuses = classify_predictions(source_text_lower, predicted_entities,
        target_entities, counts_dict)
    for word, status in words_and_statuses:
        summary_df.loc[len(summary_df)] = [str(file.name), word, status]
    return None

def evaluate():
    """Evaluate PII """
    model = 'llama3.2'
    argv = sys.argv
    if len(argv) > 1:
        model = argv[1]
    start_time = datetime.now()
    file_list, dataset, counts_dict, summary_df = init_data_structures()
    for file in Path(f"out/{model}").glob("*.json"):
        process_pii_json(file, dataset, counts_dict, summary_df)
        file_list.append(file)
    write_output(file_list, counts_dict, start_time, summary_df)

if __name__ == "__main__":
    evaluate()
