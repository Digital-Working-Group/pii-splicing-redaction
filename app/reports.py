from typing import TextIO


def generate_html_report(text: str, predicted_entities: "list[str]"):
    from rich.table import Table
    from rich.console import Console

    with open("/dev/null", "w") as f:
        console = Console(record=True, file=f)

        # # Find matches and store them
        # matches = 0
        # redactions_human = 0
        # redactions_ai = 0
        # matching_pairs = []  # Store pairs of matching values
        
        # for raw_value in raw_values:
        #     for result_value in results_values:
        #         if raw_value.lower() in result_value.lower() or result_value.lower() in raw_value.lower():
        #             matches += 1
        #             matching_pairs.append((raw_value, result_value))
        #             break
        # print(matching_pairs)

        # redactions_human = len(raw_values)
        # redactions_ai = len(results_values)
        
        # First highlight all AI found values in purple
        for value in predicted_entities:
            # Skip empty strings. Otherwise, every gap betwen characters will be filled in the .replace
            if not value:
                continue
            text = text.replace(value, f"[purple]{value}[/purple]")
        # print(f"[purple]AI found:{results_values}[/purple]")

        # # Then highlight all human values in blue
        # for value in raw_values:
        #     highlighted_text = highlighted_text.replace(value, f"[blue]{value}[/blue]")
        # print(f"[blue]Human found:{raw_values}[/blue]")

        # # Finally highlight matches in green using the stored matching pairs
        # for raw_value, result_value in matching_pairs:
        #     highlighted_text = highlighted_text.replace(f"[blue]{raw_value}[/blue]", f"[green]{raw_value}[/green]")
        #     highlighted_text = highlighted_text.replace(f"[purple]{result_value}[/purple]", f"[green]{result_value}[/green]")
        
        # Remove blank lines from highlighted text
        highlighted_text = '\n'.join(line for line in text.split('\n') if line.strip())
        
        console.print(highlighted_text)

        return console.export_html()
