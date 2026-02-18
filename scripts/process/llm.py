"""llm.py"""
import json
import re
from pathlib import Path
from typing import Any, Optional
import ollama
from scripts.config.pii_identification import Entity

def create_prompt(text: str, prompt_type: str, prompt_fp: Optional[str] = None):
    """Create a formatted prompt to identify PII entities for the given model.
    If a custom prompt is provided, use that instead.
    The prompt should have a {text} format string that will be replaced with the text to redact.
    """
    filepath = 'prompts/default_prompt.txt'
    if prompt_type == 'one_shot':
        filepath = 'prompts/one_shot_prompt.txt'
    elif prompt_type == 'few_shot':
        filepath = 'prompts/few_shot_prompt.txt'
    elif prompt_type == 'custom':
        if prompt_fp is None:
            raise FileNotFoundError('No filepath is specified for the custom prompt. Please provide a value for prompt_fp.')
        filepath = prompt_fp

    with open(filepath, 'r', encoding='utf-8') as f:
        prompt = f.read()

    return prompt.format(text=text)

MARKDOWN_EXTRACT_PATTERN = re.compile(r".*?```(?:json)?\s*(.+)```.*$", flags=re.MULTILINE | re.DOTALL)

def parse_model_output(output: str) -> "list[Entity]":
    """Parse the output of the model into a list of Entity objects.
    Raises JSONDecodeError if the model's output was unable to be parsed"""
    match = MARKDOWN_EXTRACT_PATTERN.match(output)
    if match:
        output = match.group(1)

    result: "list[Entity]" = []
    for entity in json.loads(output):
        try:
            if (
                "type" not in entity
                or not isinstance(entity["type"], str)
                or not entity["type"]
                or "value" not in entity
                or not isinstance(entity["value"], str)
                or not entity["value"]
            ):
                continue
            result.append(Entity(**entity))
        except TypeError as e:
            print(f'TypeError: {e}')
    return result

def identify_pii(text: str, model: str, options: "dict[Any, Any]") -> "list[Entity]":
    """Prompt and pass options to Ollama model and parse output."""
    response = ollama.chat(model=model, messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant helping to redact personal information. Respond in JSON.",
        },
        {
            "role": "user",
            "content": create_prompt(text, options.get('prompt_type'), options.get('prompt_fp')),
        },
    ], options=options)

    if not response.message or not response.message.content:
        raise ValueError(f"Model {model} did not return any content")
    return response

def identify_pii_from_file(input_file_path: Path, model: str, options: "dict[Any, Any]") -> "list[Entity]":
    """Converts file to text for identify_pii."""
    return identify_pii(input_file_path.read_text(), model, options)
