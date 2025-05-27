import datasets

dataset = datasets.load_dataset("ai4privacy/pii-masking-300k", data_files="data/train/1english_openpii_30k.jsonl", split="train[:500]")

for i, row in enumerate(dataset):
    with open(str(i) + ".txt", "w") as out_file:
        out_file.write(row["source_text"])
