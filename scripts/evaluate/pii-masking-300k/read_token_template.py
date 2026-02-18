"""read_token_template.py"""
def read_huggingface_token():
    """
    get token
    """
    token_loc = "YOUR PATH"
    with open(token_loc, 'r', encoding='utf-8') as infile:
        for line in infile:
            return line.strip()
    print("Key not found")
    return None