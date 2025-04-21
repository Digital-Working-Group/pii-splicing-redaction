from pathlib import Path
import json
import re

import datasets


ds = datasets.load_dataset("json", data_files="/files/hf_datasets/pii-masking-300k/data/train/1english_openpii_30k.jsonl", split="train[:500]")

total_true_positives = 0
total_false_positives = 0
total_true_negatives = 0
total_false_negatives = 0
total_non_matches = 0
error_count = 0
total_files = 0

for file in Path("out").glob("*.json"):
    row_index = int(file.name.split(".json")[0])
    # print(row_index)
    with open(file) as in_file:
        json_data = json.load(in_file)

    total_files += 1

    ds_row = ds[row_index]
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

        if is_predicted_pii and is_true_pii:
            true_positives += 1
        elif is_predicted_pii and not is_true_pii:
            false_positives += 1
        elif not is_predicted_pii and is_true_pii:
            false_negatives += 1
        else:
            true_negatives += 1

    total_true_positives += true_positives
    total_false_negatives += false_negatives
    total_true_negatives += true_negatives
    total_false_positives += false_positives
    total_non_matches += non_matches


print("TP", total_true_positives)
print("FN", total_false_negatives)
print("TN", total_true_negatives)
print("FP", total_false_positives)
print("Non matches", total_non_matches)
print("Errors", error_count)
print("Total files", total_files)