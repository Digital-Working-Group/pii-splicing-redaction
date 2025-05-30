# PII Splicing

This repository contains a tool to redact PII (personally identifiable information) using local large language models via Ollama.

# Table of Contents
1. [About Redacting PII](#about-redacting-pii)
2. [Installation without Docker](#without-docker)
3. [Installation with Docker](#with-docker)
4. [Running this tool - CLI](#running-this-tool-command-line-interface-cli)
    - [Arguments](#arguments)
    - [Usage Example](#usage-example)
5. [Running this tool - Programmatic Interface](#running-this-tool-programmatic-interface)
    - [Arguments](#arguments-1)
    - [Usage Example](#usage-example-1)
6. [Performance Metrics](#performance-metrics)
7. [Performance Testing](#performance-testing)
8. [Models](#models)
9. [Acknowledgements](#acknowledgement)
10. [Citations](#citations)

# About Redacting PII
See `main.py` and `redact_pii.py` for examples. Both will produce the same output given the same input, but `main.py` is written as a command line interface (CLI) and `redact_pii.py` uses keyword arguments via a programmatic interface. Please see the [CLI](#running-this-tool-command-line-interface-cli) and [progammatic interface](#running-this-tool-programmatic-interface) instructions respectively.

The tool expects the text to be redacted in plain text format.
Extracted entities and redacted text are outputted in JSON format.

Output files are named after the input text file, but with the extension changed from `.txt` to `.json`. For example, if the input file was named `story1.txt`, then the output file name would be `story1.json`.

# Installation
## Without Docker
These scripts require at least Python version 3.8 or later. Check your Python version via this command:
```sh
python --version
```

Install Ollama according to [the official instructions.](https://ollama.com/download)
1. Install Ollama for your OS (operating system).
2. If needed (Ollama may do this by default), add the folder containing ollama.exe to your Environment Variables.
    - On Windows: (Windows Key -> Edit environment variables for your account). Edit Path -> New -> Enter the path.
3. Verify your installation with the command:
```sh
ollama --version
```
See the [Models](#models) section below for more information on model compatibility.

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
py3-9-6_venv\Scripts\activate
```

Install requirements based on your Python version:
```sh
pip install -r py3-13-1_requirements.txt
```

## With Docker
[Docker](https://docs.docker.com/engine/install/) is required for building and running the docker container. Docker version 24.0.6, build ed223bc was used to develop and test these scripts.

Run the necessary docker build command:
```sh
docker build . -t pii_splicing
```
Run a docker container (named temp_pii_splicing):
```sh
docker run -v "$(pwd):/entry" -it --rm --name temp_pii_splicing pii_splicing
```

### GPU
If using GPUs with Docker, use the Docker `--gpus` flag before the image name. For example,
```sh
docker run --gpus=all -v "$(pwd):/entry" -it --rm --name temp_pii_splicing pii_splicing
```

# Running this tool: Command Line Interface (CLI)
## Arguments
```sh
python main.py pii_splicing [-h] [-o OUTPUT_DIR] [--write_html] [--model MODEL] [--seed SEED] [--temperature TEMPERATURE] input_paths [input_paths ...]
```
| Flag | Description | Default Value |
|---|---|---|
| -h | If included, describes the script's args. | None |
| -o | Output directory where JSON result files will be written. | "/data/output" |
| --output_format | Defines the output file type. It must either be JSON or HTML. | JSON |
| --model | The language model to use. | "llama3.2" |
| --seed | The random number seed to use for generation. | None, Ollama defaults to a random value. |
| --temperature | The temperature (creativity) of the model. | None, Ollama defaults to 0.8. |
| input_paths | List of paths to input files or directories. If a directory is specified, only files with the `.txt` extension are processed. | None |

See `main.py` for CLI script implementation.

## Usage Example
Assuming that your text files are in a folder called `sample_redaction/sample_input` and the folder `sample_redaction/sample_output` exists to store the redaction output, use the following command to use the llama3.2 model for redaction:
```sh
python main.py --model YOUR_MODEL ./YOUR_INPUT_FILEPATH -o ./YOUR_OUTPUT_FILEPATH
```
For instance, you could run:
```sh
python main.py --model llama3.2 ./sample_redaction/sample_input -o ./sample_redaction/sample_output
```
This will result in a JSON file containing the identified PII, source text, redacted text, and any errors to /sample_redaction/sample_output. 

### Sample Input and Output Files
This repository provides a sample TXT file, which can be found in `sample_redaction/sample_input/`. Each audio file's metadata is captured in a JSON and CSV file. For audio files that were generated via examples here, the parameters and functions used are also included in the metadata files. The functions used to generate the metadata files can be found in metadata.py and example usage can be seen in run_metadata.py.

# Running this tool: Programmatic Interface
## Arguments
The `redact_pii.run_redaction()`  function takes in an input paths list (`input_paths`) and a set of keyword arguments, described below.
| Keyword Argument | Type | Description | Default Value |
|---|---|---|---|
| output_dir | str | Output directory where output files (HTML or JSON) will be written. | "./sample_redaction/sample_output" |
| output_format | str | Defines the output file type. It must either be JSON or HTML. | JSON |
| model | str | The language model to use. | llama3.2 |
| seed | int | The random number seed to use for generation. | None, Ollama defaults to a random value. |
| temperature | float | The temperature (creativity) of the model. | None, Ollama defaults to 0.8. |

For more details on optional arguments, please see [Ollama's official documentation][https://ollama.readthedocs.io/en/modelfile/#valid-parameters-and-values]. To see if your version of Ollama has any different default options different from the official documentation, you can run:
```sh
ollama show --parameters YOUR-MODEL
```
See `redact_pii.py` for the script's implementation and to adjust any keyword arguments.

### Usage Example
Assuming that your text files are in a folder called `sample_redaction/sample_input` and the folder `sample_redaction/sample_output` exists to store the redaction output, use the following command to use the llama3.2 model for redaction:
```py
from redact_pii import run_redaction
run_redaction([YOUR_INPUT_FILEPATH], OPTIONAL_KWARGS)
```
For instance, you could run (please see `sample_run.py`):
```py
from redact_pii import run_redaction

def main():
    """
    main entrypoint
    """
    kwargs = {"output_dir": "./sample_redaction/sample_output", "output_format": "json", "model": "llama3.2"}
    run_redaction(["./sample_redaction/sample_input"], **kwargs)
    kwargs = {"output_dir": "./sample_redaction/sample_output", "output_format": "html", "model": "llama3.2"}
    run_redaction(["./sample_redaction/sample_input"], **kwargs)

if __name__ == '__main__':
    main()

```
The first run_redaction() call will result in a JSON file and the second will result in an HTML file. Both will contain the identified PII, source text, redacted text, and any errors to /sample_redaction/sample_output.

# Performance Metrics
If you are not already logged into the huggingface CLI from your machine, you will need to provide a user token. To do so, copy your user token into a TXT file. Then, copy the contents of `scripts/pii-masking-300k/read_token_template.py` into `scripts/pii-masking-300k/read_token.py` and edit the path in the repository to point to the text file holding your token. 

If you are using Docker, you will need to mount the file containing the token. By default, the recommended docker run commands will mount your current working directory, which may include your token file. If not, you need to mount the folder or the specific file that has the token file `docker run -v path_to_token_dir:/entry/some_dir`. Update the path in `scripts/pii-masking-300k/read_token.py` and re-run the container to mount:
```sh
docker run --gpus=all -v "$(pwd):/entry" -it --rm --name temp_pii_splicing pii_splicing
```

For more help, please see the official documentation [user tokens](https://huggingface.co/docs/hub/en/security-tokens) or the [huggingface CLI](https://huggingface.co/docs/huggingface_hub/en/guides/cli).

To evaluate the performance of this model, run the script below starting from the root of the repo:
```sh
mkdir data, out
cd data
python ../scripts/pii-masking-300k/export_pii_masking_300k.py
cd ..
python main.py --model llama3.2 ./data -o ./out
python scripts/pii-masking-300k/pii_masking_evaluate.py
```
or
```bash
mkdir data out
cd data
python3 ../scripts/pii-masking-300k/export_pii_masking_300k.py
cd ..
python3 main.py --model llama3.2 ./data -o ./out
python3 scripts/pii-masking-300k/pii_masking_evaluate.py
```
The default settings will pull 10 files from the `pii-masking-300k` dataset and write them to txt files in the /data folder. To calculate the counts for the summary, the script iterates over the source text one word at a time, comparing each word to the list of predicted entities (PII identified by the LLM) and the list of target entities (the dataset's privacy mask). Each word will be identified as one of the following:
  - True positive: found in both the target entries and the predicted entries
  - False positives: not found in the target entries, but found in the predicted entries
  - True negatives: found in neither the target entries nor the predicted entries
  - False negatives: found in the target entries, but not found in the predicted entries
If a word occurs multiple times within the text, each occurrence will be counted in the summary.

The script will output a JSON file for every TXT file containing the redacted PII, as well as two summaries in the /out/summaries folder. The summary JSON contains a list of the filenames, the starting timestamp, and the counts for each status. The summary XLSX contains columns describing the file, word, and status of that word. 

# Performance Testing
Result of Phi4 on the first 500 rows of [pii-masking-300k](https://huggingface.co/datasets/ai4privacy/pii-masking-300k), where each word in the input text is considered a separate token and identified tokens not part of the source text are ignored.
- Precision: 91.8%
- Recall: 84.6%
- F1: 88.1%

These results can be reproduced by running the [performance metric script](#performance-metrics) by adjusting the `set_size` to 500 in `scripts/pii-masking-300k/export_pii_masking_300k.py`.

# Models
Current supported models and approximate GPU VRAM requirements are:
- llama3.2 (3B parameters), 2 GB
- phi4 (14B parameters), 14 GB
- llama3.3 (70B parameters), 50 GB

Additional models can be added by modifying the Docker build to pull the new models.

# Acknowledgements
- [Ollama.](https://github.com/ollama/ollama)

# Citations
If you use this in your research, please cite the Huggingface dataset:
```bibtex
@misc{ai4privacy_2024,
	author={ Ai4Privacy },
	title={ pii-masking-300k (Revision 86db63b) },
	year=2024,
	url={ https://huggingface.co/datasets/ai4privacy/pii-masking-300k },
	doi={ 10.57967/hf/1995 },
	publisher={ Hugging Face }
}
```