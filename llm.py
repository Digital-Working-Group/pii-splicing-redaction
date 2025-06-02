"""llm.py"""
import json
import re
from pathlib import Path
from typing import Any, Optional
import ollama
from pii_identification import Entity

DEFAULT_PROMPT = """Identify personally identifiable information in the given text such as last names, usernames, dates, times, addresses, locations, IDs, emails, and sex. Return each entity as separate JSON item. Don't include items for categories not detected. Respond only with JSON, without any prefixes or suffixes.

Example input: My friends Blake Covac and John Smith used to live at Tatte at Back Bay.
Example output:
[
    {{"type": "last_name", "value": "Covac"}},
    {{"type": "last_name", "value": "Smith"}},
    {{"type": "location", "value": "Tatte at Back Bay"}}
]

Input: {text}"""

def create_prompt(text: str, custom_prompt: Optional[str]):
    """Create a formatted prompt to identify PII entities for the given model.
    If a custom prompt is provided, use that instead.
    The prompt should have a {text} format string that will be replaced with the text to redact.
    """
    if custom_prompt:
        return custom_prompt.format(text=text)
    return DEFAULT_PROMPT.format(text=text)

MARKDOWN_EXTRACT_PATTERN = re.compile(r".*?```(?:json)?\s*(.+)```.*$", flags=re.MULTILINE | re.DOTALL)

def parse_model_output(output: str) -> "list[Entity]":
    """Parse the output of the model into a list of Entity objects.
    Raises JSONDecodeError if the model's output was unable to be parsed"""
    match = MARKDOWN_EXTRACT_PATTERN.match(output)
    if match:
        output = match.group(1)

    result: "list[Entity]" = []
    for entity in json.loads(output):
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
    return result

def identify_pii(text: str, model: str, options: "dict[Any, Any]", custom_prompt: Optional[str] = None) -> "list[Entity]":
    """Prompt and pass options to Ollama model and parse output."""
    response = ollama.chat(model=model, messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant helping to redact personal information. Respond in JSON.",
        },
        {
            "role": "user",
            "content": create_prompt(text, custom_prompt),
        },
    ], options=options)

    if not response.message or not response.message.content:
        raise ValueError(f"Model {model} did not return any content")
    print(response.message.content)
    return parse_model_output(response.message.content)

def identify_pii_from_file(input_file_path: Path, model: str, options: "dict[Any, Any]", custom_prompt: Optional[str] = None) -> "list[Entity]":
    """Converts file to text for identify_pii."""
    return identify_pii(input_file_path.read_text(), model, options, custom_prompt)
