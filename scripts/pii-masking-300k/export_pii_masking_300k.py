# import datasets
from datasets import load_dataset
from read_token import read_huggingface_token

def load_hugging_face_dataset(set_size=10):
    split_str = f"train[:{set_size}]"
    try:
        return load_dataset("ai4privacy/pii-masking-300k", split=split_str)
    except FileNotFoundError:
        token = read_huggingface_token()
        return load_dataset("ai4privacy/pii-masking-300k", split=split_str, use_auth_token=token)

dataset = load_hugging_face_dataset()
for i, row in enumerate(dataset):
    with open(f"{str(i)}.txt", "w") as out_file:
        out_file.write(row["source_text"])