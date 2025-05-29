# PII Splicing

This repository contains a tool to redact PII using local large language models from Ollama.

# Table of Contents
1. [About Redacting PII](#about-redacting-pii)
2. [Installation without Docker](#installation)
3. [ Running without Docker - CLI](#command-line-interface-cli)
    - [Arguments](#arguments)
    - [Usage Example](#usage-example)
4. [Running without Docker - Programmatic Interface](#programmatic-interface)
    - [Arguments](#arguments-1)
    - [Usage Example](#usage-example-1)
5. [Performance Metrics without Docker](#performance-metrics)
6. [Installation with Docker](#installation-1)
7. [Running with Docker](#arguments-2)
    - [Arguments](#arguments-2)
    - [Usage Example](#usage-example-2)
8. [Performance Metrics with Docker](#performance-metrics-1)
9. [Models](#models)
10. [Performance Testing](#performance-testing)
11. [Acknowledgements](#acknowledgement)
12. [Citations](#citations)

# About Redacting PII
See `app/main.py` and `app/redact_pii.py` for examples. Both will produce the same output given the same input, but `app/main.py` is written to use arguments passed with flags and `app/redact_pii.py` uses keyword arguments. 

The tool expects the text to be redacted in plain text format.
Extracted entities and redacted text is output in JSON format.

Output files are named after the input text file, but with the extension changed from `.txt` to `.json`. For example, if the input file was named `story1.txt`, then the output file name would be `story1.json`.

# Without Docker
## Installation
These scripts require at least Python version 3.8 or later. Check your Python version:
```sh
python --version
```

Install Ollama according to [the official instructions](https://ollama.com/download)
1. Install Ollama for your OS.
2. Add the folder containing ollama.exe to your Environment Variables.
    - On Windows: (Windows Key -> Edit environment variables for your account). Edit Path -> New -> Enter the path.
3. Verify your installation with the command:
```sh
ollama --version
```
See the section Models below for more information on model compatibility.

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
.venv/Scripts/activate
```

Install requirements:
```sh
pip install -r requirements.txt
```

## Command Line Interface (CLI)
### Arguments
```sh
python main.py pii_splicing [-h] [-o OUTPUT_DIR] [--write_html] [--model MODEL] [--seed SEED] [--temperature TEMPERATURE] input_paths [input_paths ...]
```
| Flag | Description | Default Value |
|---|---|---|
| -h | If included, describes the script's args. | None |
| -o | Output directory where JSON result files will be written. | "/data/output" |
| --write_html | If included, generates an HTML file.  | None |
| --output_format | Defines the output file type. It must either be JSON or HTML. | JSON |
| --model | The language model to use. | "llama3.2" |
| --seed | The random number seed to use for generation. | None, Ollama default random |
| --temperature | The temperature (creativity) of the model. | None, Ollama default is 0.8 |
| input_paths | List of paths to input files or directories. If a directory is specified, only files with the `.txt` extension are processed. | None |

See `app/main.py` for CLI script implementation.

### Usage Example
Assuming that your text files are in a folder called `sample_redaction/sample_input` and the folder `sample_redactions/sample_output` exists to hold the redaction output, use the following command to use the llama3.2 model for redaction:
```sh
python app/main.py --model YOUR_MODEL ./YOUR_INPUT_FILEPATH -o ./YOUR_OUTPUT_FILEPATH
```
For instance, you could run:
```sh
python app/main.py --model llama3.2 ./sample_redaction/sample_input -o ./sample_redaction/sample_output
```
This will result in a JSON file containing the identified PII, source text, redacted text, and any errors to /sample_redaction/sample_output. 

## Programmatic Interface
### Arguments
The `app/redact_pii.run_redaction()`  function takes in an input paths list (`input_paths`) and a set of keyword arguments, described below.
| Keyword Argument | Type | Description | Default Value |
|---|---|---|---|
| output_dir | str | Output directory where JSON result files will be written. | "./sample_redaction/sample_output" |
| output_format | str | Defines the output file type. It must either be JSON or HTML. | JSON |
| model | str | The language model to use. | llama3.2 |
| seed | int | The random number seed to use for generation. | None, Ollama default is random |
| temperature | float | The temperature (creativity) of the model. | None, Ollama default is 0.8 |

For more details on optional arguments, please see [Ollama's official documentation][https://ollama.readthedocs.io/en/modelfile/#valid-parameters-and-values]. To see if your version of Ollama has any different default options different from the official documentation, you can run:
```sh
ollama show --parameters YOUR-MODEL
```
See `app/redact_pii.py` for script implementation and to adjust any key word arguments.

### Usage Example
Assuming that your text files are in a folder called `sample_redaction/sample_input` and the folder `sample_redactions/sample_output` exists to hold the redaction output, use the following command to use the llama3.2 model for redaction:
```sh
from app.redact_pii.py import run_redaction
run_redaction([YOUR_INPUT_FILEPATH], OPTIONAL_KWARGS)
```
For instance, you could run:
```sh
from app.redact_pii.py import run_redaction
kwargs = { "output_dir": "./sample_redaction/sample_output", "output_format": "json", "model": "llama3.2" }
run_redaction(["./sample_redaction/sample_input"],**kwargs)
```
This will result in a JSON file containing the identified PII, source text, redacted text, and any errors to /sample_redaction/sample_output.

## Performance Metrics
If you are not already logged into the huggingface CLI from your machine, you will need to provide a user token. To do so, copy the contents of `scripts/pii-masking-300k/read_token_template.py` into `scripts/pii-masking-300k/read_token.py` and edit the path in the repository to point to the text file holding your token. For more help, please see the official documenation [user tokens](https://huggingface.co/docs/hub/en/security-tokens) or the [huggingface CLI](https://huggingface.co/docs/huggingface_hub/en/guides/cli).

To evaluate the performance of this model, run the script below starting from the root of the repo:
```sh
mkdir data, out
cd data
python ../scripts/pii-masking-300k/export_pii_masking_300k.py
cd ..
python app/main.py --model llama3.2 ./data -o ./out
python scripts/pii-masking-300k/pii_masking_evaluate.py
```
The default settings will pull 10 files from the `pii-masking-300k` dataset and write them to txt file s in the /data folder. To calculate the counts for the summary, the script iterates over the source text one word at a time, comparing each word to the list of predicted entities (PII identified by the LLM) and the list of target entities (the dataset's privacy mask). Each word will be identified as one of the following:
  - True positive: found in both the target entries and the predicted entries
  - False positives: not found in the target entries, but found in the predicted entries
  - True negatives: found in neither the target entries nor the predicted entries
  - False negatives: found in the target entries, but not found in the predicted entries
If a word occurs multiple times within the text, each occurence will be counted in the summary.

The script will output a JSON file for every TXT file containing the redacted PII, as well as two summaries in the /out/summaries folder. The summary JSON contains a list of the filenames, the starting timestamp, and the counts different each status. The summary XLSX contains columns describing the file, word, and status of that word. 

# With Docker
## Installation
[Docker](https://docs.docker.com/engine/install/) is required for building and running the docker container. Docker version 24.0.6, build ed223bc was used to develop and test these scripts.

Run the necessary docker build command:
```sh
docker build . -t pii_splicing
```
## Arguments
```sh
docker run pii_splicing [-h] [-o OUTPUT_DIR] [--write_html] [--model MODEL] [--seed SEED] [--temperature TEMPERATURE]input_paths [input_paths ...]
```

| Flag | Description | Default Value |
|---|---|---|
| -h | If included, describes the script's args. | None |
| -o | Output directory where JSON result files will be written. | "/data/output" |
| --write_html | If included, generates an HTML file.  | None |
| --output_format | Defines the output file type. It must either be JSON or HTML. | JSON |
| --model | The language model to use. | "llama3.2" |
| --seed | The random number seed to use for generation. | None, Ollama default random |
| --temperature | The temperature (creativity) of the model. | None, Ollama default is 0.8 |
| input_paths | List of paths to input files or directories. If a directory is specified, only files with the `.txt` extension are processed. | None |

When using docker, you likely want to mount your data from the host into the container with the Docker `-v` flag. One suggested approach is to mount the text data into "/data" in the container.

See `app/main.py` for CLI script implementation.

## Usage Example
Assuming that your text files are in a folder called `sample_redaction/sample_input` and the folder `sample_redactions/sample_output` exists to hold the redaction output, use the following command to use the llama3.2 model for redaction:
```sh
docker run -v ./YOUR_FOLDER:/data pii_splicing --model YOUR_MODEL /data/YOUR_INPUT_FILEPATH
```
To use the same example as above, you could run:
```sh
docker run -v ./sample_redaction:/data pii_splicing --model llama3.2 /data/sample_input
```
If using the `run_docker.sh` file instead, you can edit the arguments listed under "Default Values". Then, run using the command:
```sh
./run_docker.sh
```

### GPU
If using GPUs with Docker, use the Docker `--gpus` flag before the image name. For example,
```sh
docker run --gpus=all -v ./redaction:/data pii_splicing --model llama3.2 /data/texts
```

## Performance Metrics
If you are not already logged into the huggingface CLI from your machine, you will need to provide a user token. To do so, please copy the contents of `scripts/pii-masking-300k/read_token_template.py` into `scripts/pii-masking-300k/read_token.py` and edit the path in the repository to point to the text file holding your token. For more help, please see the official documenation [user tokens](https://huggingface.co/docs/hub/en/security-tokens) or the [huggingface CLI](https://huggingface.co/docs/huggingface_hub/en/guides/cli).

To evaluate the performance of this model, run the script below starting from the root of the repo:
```bash
mkdir data out
cd data
python3 ../scripts/pii-masking-300k/export_pii_masking_300k.py
cd ..
docker run --gpus=all -v ./data:/input -v ./out:/output pii_splicing --model phi4 /input/ -o /output/ --output_format json
python3 scripts/pii-masking-300k/pii_masking_evaluate.py
```
The default settings will pull 10 files from the `pii-masking-300k` dataset and write them to TXT files in the /data folder. To calculate the counts for the summary, the script iterates over the source text one word at a time, comparing each word to the list of predicted entities (PII identified by the LLM) and the list of target entities (the dataset's privacy mask). Each word will be identified as one of the following:
  - True positive: found in both the target entries and the predicted entries
  - False positives: not found in the target entries, but found in the predicted entries
  - True negatives: found in neither the target entries nor the predicted entries
  - False negatives: found in the target entries, but not found in the predicted entries
If a word occurs multiple times within the text, each occurence will be counted in the summary.

The script will output a JSON file for every TXT file containing the redacted PII, as well as two summaries in the /out/summaries folder. The summary JSON contains a list of the filenames, the starting timestamp, and the counts different each status. The summary XLSX contains columns describing the file, word, and status of that word. 

# Models
Current supported models and approximate GPU VRAM requirements are:
- llama3.2 (3B parameters), 2 GB
- phi4 (14B parameters), 14 GB
- llama3.3 (70B parameters), 50 GB

Additional models can be added by modifying the Dockerbuild to pull the new models.

# Performance Testing
Result of Phi4 on the first 500 rows of [pii-masking-300k](https://huggingface.co/datasets/ai4privacy/pii-masking-300k), where each word in the input text is considered a separate token and identified tokens not part of the source text are ignored.
- Precision: 91.8%
- Recall: 84.6%
- F1: 88.1%

These results can be reproduced by running the performance metric scripts either [using Docker](#performance-metrics-1) or [without Docker](#performance-metrics) by adjusting the `set_size` to 500 in `scripts/pii-masking-300k/export_pii_masking_300k.py`.

# Acknowledgement
- [Ollama](https://github.com/ollama/ollama): Large Language Models run locally (License Ollama)

# Citations
If you use this in your research, please cite the Huggingface dataset:
```bibtex
@misc{ai4privacy_2024,
	author       = { Ai4Privacy },
	title        = { pii-masking-300k (Revision 86db63b) },
	year         = 2024,
	url          = { https://huggingface.co/datasets/ai4privacy/pii-masking-300k },
	doi          = { 10.57967/hf/1995 },
	publisher    = { Hugging Face }
}
```