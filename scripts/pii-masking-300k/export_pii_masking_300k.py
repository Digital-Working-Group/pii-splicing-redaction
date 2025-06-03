"""export_pii_masking_300k.py"""
from datasets import load_dataset
from read_token import read_huggingface_token

def load_hugging_face_dataset(set_size=10):
    """Load pii-masking-300k dataset from hugging face"""
    split_str = f"train[:{set_size}]"
    try:
        return load_dataset("ai4privacy/pii-masking-300k", split=split_str)
    except FileNotFoundError:
        token = read_huggingface_token()
        return load_dataset("ai4privacy/pii-masking-300k", split=split_str, use_auth_token=token)

def export_pii_masking():
    """Write pii-masking-300k dataset from hugging face as txt files"""
    dataset = load_hugging_face_dataset()
    for i, row in enumerate(dataset):
        with open(f"{str(i)}.txt", "w", encoding="utf-8") as out_file:
            out_file.write(row["source_text"])

if __name__ == "__main__":
    export_pii_masking()
