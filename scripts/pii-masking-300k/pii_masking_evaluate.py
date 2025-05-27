from pathlib import Path
import json
import re
import os
import pandas as pd
from export_pii_masking_300k import load_hugging_face_dataset
from datasets import load_dataset
from datetime import datetime

start_time = datetime.now()

dataset = load_hugging_face_dataset()
file_list = []
summary_df = pd.DataFrame(columns=['filename', 'predicted_word', 'status'])

total_true_positives = 0
total_false_positives = 0
total_true_negatives = 0
total_false_negatives = 0
total_non_matches = 0
error_count = 0
total_files = 0


for file in Path("out").glob("*.json"):
    file_list.append(file.name)
    row_index = int(file.name.split(".json")[0])
    # print(row_index)
    with open(file) as in_file:
        json_data = json.load(in_file)

    total_files += 1

    ds_row = dataset[row_index]
    if "errors" in ds_row:
        error_count += 1

    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0
    non_matches = 0

    target_entities = set()
    for entity in ds_row["privacy_mask"]:
        for word in re.split(r"[^a-zA-Z0-9]+", entity["value"]):
            target_entities.add(word.lower())

    source_text_lower = ds_row["source_text"].lower()

    predicted_entities = set()
    for predicted_entity in json_data["entities"]:
        for word in re.split(r"[^a-zA-Z0-9]+", predicted_entity["value"]):
            print("Predicted word", word)
            word = word.lower()
            predicted_entities.add(word.lower())
            if word not in source_text_lower:
                non_matches += 1

    print(target_entities)

    print(ds_row["privacy_mask"])
    print(ds_row["source_text"])


    for word in re.split(r"[^a-zA-Z0-9]+", ds_row["source_text"]):
        word = word.lower()

        is_predicted_pii = word in predicted_entities
        is_true_pii = word in target_entities
        
        status = ''
        if is_predicted_pii and is_true_pii:
            true_positives += 1
            status = "true_positives"
        elif is_predicted_pii and not is_true_pii:
            false_positives += 1
            status = "false_positives"
        elif not is_predicted_pii and is_true_pii:
            false_negatives += 1
            status = "false_negatives"
        else:
            true_negatives += 1
            status = "true_negatives"

        summary_df.loc[len(summary_df)] = [str(file.name), word, status]

    total_true_positives += true_positives
    total_false_negatives += false_negatives
    total_true_negatives += true_negatives
    total_false_positives += false_positives
    total_non_matches += non_matches


print("TP", total_true_positives)
print("TN", total_true_negatives)
print("FP", total_false_positives)
print("FN", total_false_negatives)
print("Non matches", total_non_matches)
print("Errors", error_count)
print("Total files", total_files)


summary = {
    "True Positives": total_true_positives,
    "True Negatives": total_true_negatives,
    "False Positives": total_false_positives,
    "False Negatives": total_false_negatives,
    "Non matches": total_non_matches,
    "Errors": error_count,
    "Total files": total_files,
    "Files": file_list,
    "Ran at": start_time.strftime("%Y-%m-%d %H:%M:%S")
}

print(summary)
print(summary_df)

script_dir = Path(__file__).resolve().parent
output_root = script_dir.parent.parent / "out/summaries"
output_root.mkdir(parents=True, exist_ok=True)
json_fp = os.path.join(output_root, f'summary_{start_time.strftime("%Y%m%d_%H%M%S")}.json')
with open(json_fp, 'w') as fp:
    json.dump(summary, fp, default=str, indent=4)

xlsx_fp = os.path.join(output_root, f'summary_{start_time.strftime("%Y%m%d_%H%M%S")}.xlsx')
writer = pd.ExcelWriter(xlsx_fp, engine='xlsxwriter')
summary_df.to_excel(writer, sheet_name='Summary', index=False)
for group, data in summary_df.groupby(['filename']):
    tech_id = group[0]
    data.drop(labels='filename', axis=1, inplace=True)
    data.to_excel(writer, sheet_name=tech_id, index=False)
writer.close()