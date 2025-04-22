# PII Splicing

This repository contains a tool to redact PII using local large language models from Ollama.

# Installation
## Without Docker

First, install Ollama according to [the official instructions](https://ollama.com/download)

Python at least version 3.8 is required.
The requirements.txt file can be used to install the necessary libraries without Docker.

Create and activate a virtual environment:
```sh
python3 -m venv .venv
. .venv/bin/activate
```

Install requirements:
```sh
python3 -m venv install -r requirements.txt
```

### With Docker

Build with
```sh
docker build . -t pii_splicing
```

# Usage

The tool expects the text to be redacted in plain text format.
Extracted entities and redacted text is output in JSON format.

Output files are named after the input text file, but with the extension changed
from `.txt` to `.json`. For example, if the input file was named `story1.txt`,
then the output file name would be `story1.json`.

When using docker, you likely want to mount your data from the host into the
container with the Docker `-v` flag.
One suggested approach is to mount the text data into "/data" in the container.

Arguments:
```sh
docker run pii_splicing [-h] [-o OUTPUT_DIR] [--write_html] [--model MODEL] input_paths [input_paths ...]
```
or
```sh
python3 main.py pii_splicing [-h] [-o OUTPUT_DIR] [--write_html] [--model MODEL] input_paths [input_paths ...]
```
- `input_paths` is a list of paths to input files or directories. If a directory is specified, only files with the `.txt` extension are processed
- `-o` is the output directory to where JSON result files will be written. Default is `/data/output`
- `--model` is the language model to use. See

## Usage Example
Assuming that your text files are in a folder called `redaction/texts` and
the folder `redaction/output` exists to hold the redaction output,
use this command to use the llama3.2 model for redaction:
```sh
docker run -v ./redaction:/data pii_splicing --model llama3.2 /data/texts
```

Output JSON files will be in `redaction/output`.

If not using Docker,
```sh
python3 app/main.py --model llama3.2 ./redaction/texts -o ./redaction/output
```

### GPU
If using GPUs with Docker, use the Docker `--gpus` flag before the image name. For example,
```sh
docker run --gpus=all -v ./redaction:/data pii_splicing --model llama3.2 /data/texts
```

# Models
Current supported models are
- llama3.2 (3B parameters)
- phi4 (14B parameters)
- llama3.3 (70B parameters)

Additional models can be added by modifying the Dockerbuild to pull the new models.

# Performance metrics
Result of Phi4 on the first 500 rows of [https://huggingface.co/datasets/ai4privacy/pii-masking-300k](pii-masking-300k), where each word in the input text is considered a separate token and identified tokens not part of the source text are ignored.
- Precision: 91.8%
- Recall: 84.6%
- F1: 88.1%

These results can be reproduced by first exporting the dataset as text files with `scripts/pii-masking-300k/export_pii_masking.py`. Next, run the app through the generated files. Finally, run scripts `scripts/pii-masking-300k/pii_masking_evaluation.py`