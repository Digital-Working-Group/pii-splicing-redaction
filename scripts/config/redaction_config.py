"""redaction_config.py"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class RedactionConfig:
    output_dir: str = "./sample_redaction/sample_output"
    output_format: str = "json"
    model: str = "llama3.2"
    prompt_type: str = "default"
    num_runs: int = 1
    aggregation: Optional[str] = None
    threshold: Optional[float] = None
    temperature: Optional[float] = None
    seed: Optional[int] = None
    prompt_fp: Optional[str] = None
    options: dict = field(default_factory=dict)

    def __post_init__(self):
        """Convert types and build options dict"""
        self.output_dir_path = Path(self.output_dir)
        
        # Build options dict
        self.options.update({
            "prompt_type": self.prompt_type,
            "num_runs": self.num_runs,
        })
        
        # Add optional typed fields
        if self.aggregation is not None:
            self.options["aggregation"] = self.aggregation
        if self.threshold is not None:
            self.options["threshold"] = self.threshold
        if self.temperature is not None:
            self.options["temperature"] = self.temperature
        if self.seed is not None:
            self.options["seed"] = self.seed
        if self.prompt_fp is not None:
            self.options["prompt_fp"] = self.prompt_fp
