# PII Splicing Redaction

This repository contains a tool to redact PII (personally identifiable information) using local large language models via Ollama. Please see the [pii-splicing-documentation](https://github.com/Digital-Working-Group/pii-splicing-documentation) repository for further reading materials on PII Splicing.

# Table of Contents
1. [Introduction](#introduction)
2. [Installation without Docker](#without-docker)
3. [Installation with Docker](#with-docker)
4. [Running this tool - CLI](#running-this-tool-command-line-interface-cli)
    - [Arguments](#arguments)
    - [Usage Example](#usage-example)
5. [Running this tool - Programmatic Interface](#running-this-tool-programmatic-interface)
    - [Arguments](#arguments-1)
    - [Usage Example](#usage-example-1)
6. [Calculate Performance Metrics on pii-masking-300k](#calculate-performance-metrics-on-pii-masking-300k)
7. [Performance Metrics on pii-masking-300k](#performance-metrics-on-pii-masking-300k))
8. [Models](#models)
9. [Acknowledgements](#acknowledgement)
10. [Citations](#citations)

# Introduction
See `main.py` and `redact_pii.py` for examples. Both will produce the same output given the same input, but `main.py` is written as a command line interface (CLI) and `redact_pii.py` uses keyword arguments via a programmatic interface. Please see the [CLI](#running-this-tool-command-line-interface-cli) and [progammatic interface](#running-this-tool-programmatic-interface) instructions respectively.

## Sample Input and Output Files
The tool expects plain text files as input. Extracted entities and redacted text are written in JSON or HTML format, based on the selected output format. Output files will be written to a directory named after the LLM model that was selected.

A sample input file can be found in `sample_redaction/sample_input/`. Sample output files (JSON and HTML) from utilizing the llama3.2 model can be found in `sample_redaction/sample_output/llama3.2`. Sample raw LLM response output files can be found in `sample_redaction/sample_output/llama3.2/llm_raw_response/<output_filename>-<output_file_extension>.json`.

```
sample_redaction
   |-- sample_input
   |   |-- test.txt
   |-- sample_output
   |   |-- llama3.2
   |   |   |-- llm_raw_response
   |   |   |   |-- test-html.json
   |   |   |   |-- test-json.json
   |   |   |-- test.html
   |   |   |-- test.json

```

### Sample Input File
Please see the plain text file [test.txt](sample_redaction/sample_input/test.txt) for an example of an input file.

### Sample Output Files
See `process_file_json_out()` and `process_file_html_out()` in [process_out.py](process_out.py) for full details on how the output JSON/HTML files are created.

The [test.json](sample_redaction/sample_output/llama3.2/test.json) file contains:
- An `entities` key, which contains a parsed list of dictionaries, where `type` contains the category of PII that was identified and `value` contains the words that comprise the identified PII.
- A `source_text` key, which contains the original text from the input file.
- A `redacted_text` key, which contains the source text from the input file, but with `<PII>` replacing all the identified PII entities (see `redact_text()` in [redaction.py](redaction.py).
- An `errors` key, which will contain a string of the error message that occurred when trying to parse the model's LLM output. The `entities` list should be empty if errors is not an empty list. If an error occurs, the llm_raw_response file is still created.

The [test.html](sample_redaction/sample_output/llama3.2/test.html) file contains <...>.

The [test-html.json](sample_redaction/sample_output/llama3.2/llm_raw_response/test-html.json) and [test-json.json](sample_redaction/sample_output/llama3.2/llm_raw_response/test-json.json) files contain the raw LLM response when running the tool with llama3.2 on test.html and test.json respectively. See `llm_message_out()` in [process_out.py](process_out.py) for further details.

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
4. Pull the necessary model(s) for usage via Ollama. This should only need to be run once:

```sh
ollama pull llama3.2
```

See the [Models](#models) section below for more information on a few models.

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
python main.py input_paths [input_paths ...] [-h] [-o OUTPUT_DIR] [--model MODEL] [--output_format OUTPUT_FORMAT] [--temperature TEMPERATURE] [--seed SEED] 
```
| Flag | Description | Default Value |
|---|---|---|
| input_paths | List of paths to input files or directories. If a directory is specified, only files with the `.txt` extension are processed. | None |
| -h | If included, describes the script's args. | None |
| -o | Output directory where JSON result files will be written. | "/data/output" |
| --model | The language model to use. | "llama3.2" |
| --output_format | Defines the output file type. It must either be JSON or HTML. | JSON |
| --temperature | The temperature (creativity) of the model. | None, Ollama defaults to 0.8. |
| --seed | The random number seed to use for generation. | None, Ollama defaults to a random value. |

See [main.py](main.py) for details on the CLI script implementation.

## Usage Example
Assuming that your text files are in a folder called `sample_redaction/sample_input` and the folder `sample_redaction/sample_output` exists to store the redaction output, use the following command to use the llama3.2 model for redaction:
```sh
python main.py --model YOUR_MODEL ./YOUR_INPUT_FILEPATH -o ./YOUR_OUTPUT_FILEPATH
```
For instance, you could run:
```sh
python main.py --model llama3.2 ./sample_redaction/sample_input -o ./sample_redaction/sample_output
```
See [Sample Input and Output Files](#sample-input-and-output-files) for more information on input and output files.

# Running this tool: Programmatic Interface
## Arguments
The `redact_pii.run_redaction()`  function takes in an input paths list (`input_paths`) and a set of keyword arguments, described below.
| Keyword Argument | Type | Description | Default Value |
|---|---|---|---|
| output_dir | str | Output directory where output files (HTML or JSON) will be written. | "./sample_redaction/sample_output" |
| output_format | str | Defines the output file type. It must either be JSON or HTML. | JSON |
| model | str | The language model to use. | llama3.2 |
| temperature | float | The temperature (creativity) of the model. | None, Ollama defaults to 0.8. |
| seed | int | The random number seed to use for generation. | None, Ollama defaults to a random value. |

For more details on optional arguments, please see [Ollama's official documentation](https://ollama.readthedocs.io/en/modelfile/#valid-parameters-and-values). To see if your model via Ollama has any different default options different from the official documentation, you can run:

```sh
ollama show --parameters YOUR-MODEL
```
See [redact_pii.py](redact_pii.py) for the script's implementation and to adjust any keyword arguments.

### Usage Example
Assuming that your text files are in a folder called `sample_redaction/sample_input` and the folder `sample_redaction/sample_output` exists to store the redaction output, use the following command to use the llama3.2 model for redaction:
```py
from redact_pii import run_redaction
run_redaction([YOUR_INPUT_FILEPATH], OPTIONAL_KWARGS)
```
For instance, you could run (please see [sample_run.py](sample_run.py)):
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
See [Sample Input and Output Files](#sample-input-and-output-files) for more information on input and output files.

# Calculate Performance Metrics on pii-masking-300k
If you are not already logged into the Hugging Face CLI from your machine, you will need to provide a user token. To create and access your user token, follow the steps below:
1. Go to [Hugging Face's user token page](https://huggingface.co/settings/tokens)
2. Create a new token 
3. Select the token type **Read**, enter a token name, and then create the token
4. Copy the token into a text file 
5. Create a new file called `scripts/pii-masking-300k/read_token.py` and copy the contents of `scripts/pii-masking-300k/read_token_template.py` into it
6. Edit the `token_loc` variable in the `read_token.py` script to point to the text file holding your token

If you are using Docker, you will need to mount the file containing the token. By default, the recommended docker run commands will mount your current working directory, which may include your token file. If not, you need to mount the folder or the specific file that has the token file `docker run -v path_to_token_dir:/entry/some_dir`. Update the path in `scripts/pii-masking-300k/read_token.py` and re-run the container to mount:
```sh
docker run --gpus=all -v "$(pwd):/entry" -it --rm --name temp_pii_splicing pii_splicing
```

For more help, please see the official documentation [user tokens](https://huggingface.co/docs/hub/en/security-tokens) or the [Hugging Face CLI](https://huggingface.co/docs/huggingface_hub/en/guides/cli).

To evaluate the performance of this model, run the commands below in the root of the repo (python3 may be needed instead of python, depending on the environment):

```sh
mkdir data out
cd data
python ../scripts/pii-masking-300k/export_pii_masking_300k.py
cd ..
python main.py --model llama3.2 ./data -o ./out
python scripts/pii-masking-300k/pii_masking_evaluate.py
```

The default settings in [export_pii_masking_300k.py](scripts/pii-masking-300k/export_pii_masking_300k.py) will pull 10 files (see `set_size` in load_hugging_face_dataset()) from the `pii-masking-300k` dataset and write them to txt files in the data/ folder (0.txt, 1.txt, ...).

By default, [pii_masking_evaluate.py](scripts/pii-masking-300k/pii_masking_evaluate.py) will iterate over the contents `out/llama3.2` for JSON files (see `evaluate()`). A different model name can be supplied to pii_masking_evaluate.py to iterate over that directory instead.

```sh
python scripts/pii-masking-300k/pii_masking_evaluate.py ## targets out/llama3.2
python scripts/pii-masking-300k/pii_masking_evaluate.py llama3.2 ## targets out/llama3.2
python scripts/pii-masking-300k/pii_masking_evaluate.py phi4 ## targets out/phi4
```

To calculate the counts for the summary, the script iterates over the source text one word at a time, comparing each word to the list of predicted entities (PII identified by the LLM) and the list of target entities (the dataset's privacy mask). If a word occurs multiple times within the text, each occurrence will be counted in the summary.

Each word will be identified as one of the following:
  - True positive: found in both the target entries and the predicted entries
  - False positive: not found in the target entries, but found in the predicted entries
  - True negative: found in neither the target entries nor the predicted entries
  - False negative: found in the target entries, but not found in the predicted entries
  - Precision: True positives / (True positives + False positives)
  - Recall: True positives / (True positives + False negatives)
  - F1: 2 * Precision * Recall / (Precision + Recall)

## Output Files
```
out
   |-- llama3.2
   |   |-- llm_raw_response
   |   |   |-- 0-json.json
   |   |   |-- 1-json.json ## N-json.json for every input file
   |   |-- summaries
   |   |   |-- summary_YYYYMMDD_HHMMSS.json
   |   |   |-- summary_YYYYMMDD_HHMMSS.xlsx
   |   |-- 0.json
   |   |-- 1.json ## N.json for every input file

```
Further information on the structure of the output files can be seen in the [Sample Output Files](#sample-output-files) section.

The `out/llama3.2/` directory will contain:
- The output JSON files (0.json, 1.json, ...9.json) from the PII redaction (same structure as [test.json](sample_redaction/sample_output/llama3.2/test.json)).
- A `llm_raw_response/` folder that contains the raw LLM response for each respective input file (same structure as [test-json.json](sample_redaction/sample_output/llama3.2/llm_raw_response/test-json.json)).
- A `summaries/` folder that contains:
    - A timestamped `summary_YYYY_MM_DD_HHMMSS.json` file that contains the performance metrics and other information. (see `write_summary_json()` in [pii_masking_evaluate.py](scripts/pii-masking-300k/pii_masking_evaluate.py))
    - A timestamped `summary_YYYY_MM_DD_HHMMSS.xlsx` file that contains a Summary tab, and then individual tabs for each output JSON file that had no errors. (see `write_summary_xlsx()`in [pii_masking_evaluate.py](scripts/pii-masking-300k/pii_masking_evaluate.py))

# Performance Metrics on pii-masking-300k
Results of the Phi4 LLM model on the first 500 rows of [pii-masking-300k](https://huggingface.co/datasets/ai4privacy/pii-masking-300k).

- Precision: 91.8%
- Recall: 84.6%
- F1: 88.1%

These results can be reproduced by running the [performance metric script](#performance-metrics) by adjusting the `set_size` to 500 in `scripts/pii-masking-300k/export_pii_masking_300k.py`. There were N=31 predicted words that were non-matches (not in the original text).

# Models
Current supported models and approximate GPU VRAM requirements are:
- llama3.2 (3B parameters), 2 GB
- phi4 (14B parameters), 14 GB
- llama3.3 (70B parameters), 50 GB

Additional LLM models can be pulled down via ollama, see the [ollama library here](https://ollama.com/library).

# Acknowledgements
- [Ollama.](https://github.com/ollama/ollama)

# Citations
If you use this in your research, please cite the Hugging Face dataset:
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