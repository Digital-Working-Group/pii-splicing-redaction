# PII Splicing

This repository contains a tool to redact PII using local large language models from Ollama.

# Installation
## Without Docker

First, install Ollama according to [the official instructions](https://ollama.com/download)
1. Install Ollama for your OS.
2. Add the folder containing ollama.exe to your Environment Variables.
    - On Windows: (Windows Key -> Edit environment variables for your account). Edit Path -> New -> Enter the path.
3. Verify your installation with the command
```sh
ollama --version
```
4. Download the desired model with the command
```sh
ollama run llama3.2
```
See the section Models below for more information on model compatibility.

These scripts require at least Python version 3.8 or later. Check your Python version:
```sh
python --version
```

The requirements.txt file can be used to install the necessary libraries to a virtual environment without Docker.

Create a virtual environment:
```sh
python -m venv .venv
```

Activate your virtual environment:
```sh
.venv/bin/activate
```

or with Windows:
```sh
.venv\Scripts\activate
```

Install requirements:
```sh
pip install -r requirements.txt
```

### With Docker
[Docker](https://docs.docker.com/engine/install/) is required for building and running the docker container. Docker version 24.0.6, build ed223bc was used to develop and test these scripts.

Run the necessary docker build commands provided in the `build_docker.sh` and `run_docker.sh` scripts. These .sh scripts were tested on Linux (CentOS 7).
```sh
docker build . -t pii_splicing
```

# Redacting PII
See `app/main.py` and `app/redact_pii.py` for examples. Both will produce the same output given the same input, but `app/main.py` is written to use arguments passed with flags and `app/redact_pii.py` uses keyword arguments. 

The tool expects the text to be redacted in plain text format.
Extracted entities and redacted text is output in JSON format.

Output files are named after the input text file, but with the extension changed
from `.txt` to `.json`. For example, if the input file was named `story1.txt`,
then the output file name would be `story1.json`.

When using docker, you likely want to mount your data from the host into the
container with the Docker `-v` flag.
One suggested approach is to mount the text data into "/data" in the container.

## Arguments in `app/main.py`:
```sh
docker run pii_splicing [-h] [-o OUTPUT_DIR] [--write_html] [--model MODEL] input_paths [input_paths ...]
```
or
```sh
python3 main.py pii_splicing [-h] [-o OUTPUT_DIR] [--write_html] [--model MODEL] input_paths [input_paths ...]
```

| Flag | Description | Default Value |
|---|---|---|---|
| -h | If included, describes the script's args. | None |
| -o | Output directory where JSON result files will be written. | "/data/output" |
| --write_html | If included, generates an html file.  | None |
| --output_format | Defines the output file type. It must either be .json or .html. | .json |
| --model | The language model to use. | "llama3.2" |
| input_paths | List of paths to input files or directories. If a directory is specified, only files with the `.txt` extension are processed. | None |

## Arguments in `app/redact_pii.py`:
The `app/redact_pii.run_redaction()`  function takes in an input paths list (`input_paths`) and a set of keyword arguments:
| Keyword Argument | Type | Description | Default Value |
|---|---|---|---|
| output_dir | str | Output directory where JSON result files will be written. | "./data/output" |
| output_format | str | Defines the output file type. It must either be JSON or HTML | JSON |
| model | The language model to use. | llama3.2 |

## Usage Example
Assuming that your text files are in a folder called `sample_redaction/sample_input` and
the folder `sample_redactions/sample_output` exists to hold the redaction output,
use the commands below to use the llama3.2 model for redaction.
With Docker:
```sh
docker run -v ./sample_redaction:/data pii_splicing --model llama3.2 /data/sample_input
```

If not using Docker,
```sh
python3 app/main.py --model llama3.2 ./sample_redcaction/sample_input -o ./sample_redcaction/sample_output
```
Output JSON files will be in ./sample_redcaction/sample_input.

If using keyword arguments instead, you could perform the same actions above by running the following commands:
```sh
from app/redact_pii.py import run_redaction
kwargs = { "output_dir": "./sample_redaction/sample_output", "output_format": "json", "model": "llama3.2" }
run_redaction(["./sample_redcaction/sample_input"],**kwargs)
```

All three examples will output a JSON file to /sample_redcaction/sample_input. 

### GPU
If using GPUs with Docker, use the Docker `--gpus` flag before the image name. For example,
```sh
docker run --gpus=all -v ./redaction:/data pii_splicing --model llama3.2 /data/texts
```

# Models
Current supported models and approximate GPU VRAM requirements are:
- llama3.2 (3B parameters), 2 GB
- phi4 (14B parameters), 14 GB
- llama3.3 (70B parameters), 50 GB

Additional models can be added by modifying the Dockerbuild to pull the new models.

# Performance metrics
Result of Phi4 on the first 500 rows of [https://huggingface.co/datasets/ai4privacy/pii-masking-300k](pii-masking-300k), where each word in the input text is considered a separate token and identified tokens not part of the source text are ignored.
- Precision: 91.8%
- Recall: 84.6%
- F1: 88.1%

These results can be reproduced by first exporting the dataset as text files with `scripts/pii-masking-300k/export_pii_masking.py`. Next, run the app over the generated files to make predictions with the models on each row. Finally, run scripts `scripts/pii-masking-300k/pii_masking_evaluation.py`.

Run this script in the root of the repo:
```bash
mkdir data out
cd data
python3 ../scripts/pii-masking-300k/export_pii_masking_300k.py
cd ..
docker run --gpus=all -v ./data:/input -v ./out:/output pii_splicing --model phi4 /input/ -o /output/ --output_format html
python3 scripts/pii_masking_evaluate.py
```