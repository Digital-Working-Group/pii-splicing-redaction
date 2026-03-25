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
6. [Multiple Runs](#multiple-runs)
7. [Calculate Performance Metrics on pii-masking-300k](#calculate-performance-metrics-on-pii-masking-300k)
8. [Performance Metrics on pii-masking-300k](#performance-metrics-on-pii-masking-300k)
9. [Models](#models)
10. [Acknowledgements](#acknowledgements)
11. [Citations](#citations)

# Introduction
See [main.py](main.py) and [redact_pii.py](redact_pii.py) for examples. Both will produce the same output given the same input, but [main.py](main.py) is written as a command line interface (CLI) and [redact_pii.py](redact_pii.py) uses keyword arguments via a programmatic interface. Please see the [CLI](#running-this-tool-command-line-interface-cli) and [progammatic interface](#running-this-tool-programmatic-interface) instructions respectively.

## Sample Input and Output Files
The tool expects plain text files as input. Optionally, the tool accepts a custom prompt to instruct the LLM, otherwise using the pre-written prompts. Extracted entities and redacted text are written in JSON or HTML format, based on the selected output format. Output files will be written to a directory named after the LLM model that was selected.

A sample input file can be found in `sample_redaction/sample_input/`. Sample output files (JSON and HTML) from utilizing the llama3.2 model can be found in `sample_redaction/sample_output/llama3.2`. Sample raw LLM response output files can be found in `sample_redaction/sample_output/llama3.2/<prompt_type>/llm_raw_response/<output_filename>-<output_file_extension>.json`.

```
sample_redaction
   |-- sample_input
   |   |-- test.txt
   |-- sample_output
   |   |-- default
   |   |   |-- llama3.2
   |   |   |   |-- llm_raw_response
   |   |   |   |   |-- test_0-html.json
   |   |   |   |   |-- test_0-json.json
   |   |   |   |   |-- test_1-html.json
   |   |   |   |   |-- test_1-json.json
   |   |   |   |   |-- test_2-html.json
   |   |   |   |   |-- test_2-json.json
   |   |   |   |   |-- test_3-html.json
   |   |   |   |   |-- test_3-json.json
   |   |   |   |-- test_0.html
   |   |   |   |-- test_0.json
   |   |   |   |-- test_1.html
   |   |   |   |-- test_1.json
   |   |   |   |-- test_2.html
   |   |   |   |-- test_2.json
   |   |   |   |-- test_3.html
   |   |   |   |-- test_3.json
   |   |   |   |-- test_lenient.html
   |   |   |   |-- test_lenient.json
   |   |   |   |-- test_majority.html
   |   |   |   |-- test_majority.json
   |   |   |   |-- test_restrictive.html
   |   |   |   |-- test_restrictive.json
   |   |   |   |-- test_threshold.html
   |   |   |   |-- test_threshold.json
   

```

### Sample Input File
Please see the plain text file [test.txt](sample_redaction/sample_input/test.txt) for a sample input file.

### Sample Prompt
Please see the [prompts](prompts/) for the provided prompt options or [sample_custom_prompt.txt](prompts/sample_custom_prompt.txt) for a template to create a custom prompt.

### Sample Output Files
See `process_file_json_out()` and `process_file_html_out()` in [process_out.py](./scripts/process/process_out.py) for full details on how the output JSON/HTML files are created.

An output JSON file, for example [test_0.json](sample_redaction/sample_output/llama3.2/default/test/test_0.json) contains:
- An `entities` key, which contains a parsed list of dictionaries, where `type` contains the category of PII that was identified and `value` contains the words that comprise the identified PII.
- A `source_text` key, which contains the original text from the input file.
- A `redacted_text` key, which contains the source text from the input file, but with `<PII>` replacing all the identified PII entities (see `redact_text()` in [redaction.py](redaction.py)).
- An `errors` key, which will contain a string of the error message that occurred when trying to parse the model's LLM output. The `entities` list should be empty if errors is not an empty list. If an error occurs, the llm_raw_response file is still created.

An output HTML file, for example [test_0.html](sample_redaction/sample_output/llama3.2/default/test/test_0.html), contains the text from the input file with the predicted entities in purple.

The [test_0-html.json](sample_redaction/sample_output/llama3.2/default/test/llm_raw_response/test_0-html.json) and [test_0-json.json](sample_redaction/sample_output/llama3.2/default/test/llm_raw_response/test_0-json.json) files contain the raw LLM response when running the tool with llama3.2 on test.html and test.json respectively. See `llm_message_out()` in [process_out.py](./scripts/process/process_out.py) for further details.

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

Enter the requirements directory:
```sh
cd requirements
```

Run the necessary docker build command:
```sh
docker build . -t pii_splicing
```
Run a docker container (named temp_pii_splicing):
```sh
docker run -v "$(dirname "$(pwd)"):/entry" -it --rm --name temp_pii_splicing pii_splicing
```

### GPU
If using GPUs with Docker, use the Docker `--gpus` flag before the image name. For example,
```sh
docker run --gpus=all -v "$(dirname "$(pwd)"):/entry" -it --rm --name temp_pii_splicing pii_splicing
```
## Jupyter Notebook Examples

Please run [jupyter notebook](https://docs.jupyter.org/en/latest/running.html) and see [Pii_Splicing_Redaction_Example_Usage.ipynb](Pii_Splicing_Redaction_Example_Usage.ipynb) for an interactive set of examples. Also, see the usage example sections below.

# Running this tool: Command Line Interface (CLI)
## Arguments
```sh
python main.py -h
usage: main.py [-h] [-o OUTPUT_DIR] [--model MODEL] [--output_format {json,html}]
               [--num_runs NUM_RUNS] [--temperature TEMPERATURE] [--seed SEED]
               [--prompt_type PROMPT_TYPE] [--prompt_fp PROMPT_FP]
               [--aggregation {restrictive,threshold,majority,lenient}] [--threshold THRESHOLD]
               input_paths [input_paths ...]

positional arguments:
  input_paths

options:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
  --model MODEL
  --output_format {json,html}
  --num_runs NUM_RUNS
  --temperature TEMPERATURE
  --seed SEED
  --prompt_type PROMPT_TYPE
  --prompt_fp PROMPT_FP
  --aggregation {restrictive,threshold,majority,lenient}
  --threshold THRESHOLD
```
| Flag | Description | Default Value |
|---|---|---|
| input_paths | List of paths to input files or directories. If a directory is specified, only files with the `.txt` extension are processed. | None |
| -h | If included, describes the script's args. | None |
| -o | Output directory where JSON result files will be written. | "/data/output" |
| --model | The language model to use. | "phi4 |
| --output_format | Defines the output file type. It must either be JSON or HTML. | JSON |
| --temperature | The temperature (creativity) of the model. | None, Ollama defaults to 0.8. |
| --seed | The random number seed to use for generation. | None, Ollama defaults to a random value. |
| --num_runs | The number of times to run the redaction on each file. | 1 |
| --prompt_type | Prompt to be passed to the LLM. (Options: "default", "few_shot", "one_shot", "custom") | "default" |
| --prompt_fp | If prompt_type is "custom", provide the path the the TXT file. | None |
| --aggregation | If num_runs > 1, the aggregation method used to summarize the runs for each file. (Options: "restrictive", "threshold", "majority", "lenient") | "restrictive" |
| --threshold | If aggregation type is "threshold", the threshold desired (i.e. 0.35, 0.75) | 0.5 |

See [main.py](main.py) for details on the CLI script implementation.

## Usage Example
Assuming that your text files are in a folder called `sample_redaction/sample_input` and the folder `sample_redaction/sample_output` exists to store the redaction output, use the following command to use the llama3.2 model for redaction:
```sh
cd scripts
python main.py --model YOUR_MODEL ./YOUR_INPUT_FILEPATH -o ./YOUR_OUTPUT_FILEPATH
```
For instance, you could run:
```sh
cd scripts
python main.py --model phi4 ../sample_redaction/sample_input -o ../sample_redaction/sample_output
```

```sh
cd scripts
python main.py --model phi4 --num_runs 3 --prompt_type default --aggregation restrictive ../sample_redaction/sample_input -o ../sample_redaction/sample_output
```

```sh
cd scripts
python main.py --model phi4 --num_runs 3 --prompt_type default --aggregation threshold --threshold 0.25 ../sample_redaction/sample_input -o ../sample_redaction/sample_output
```

```sh
cd scripts
python main.py --model phi4 --num_runs 3 --prompt_type default --aggregation majority ../sample_redaction/sample_input -o ../sample_redaction/sample_output
```

```sh
cd scripts
python main.py --model phi4 --num_runs 3 --prompt_type default --aggregation lenient ../sample_redaction/sample_input -o ../sample_redaction/sample_output
```

See [Sample Input and Output Files](#sample-input-and-output-files) for more information on input and output files.

# Running this tool: Programmatic Interface
## Arguments
The `scripts.process.redaction.run_redaction()`  function takes in an input paths list (`input_paths`) and a set of keyword arguments, described below.
| Keyword Argument | Type | Description | Default Value |
|---|---|---|---|
| output_dir | str | Output directory where output files (HTML or JSON) will be written. | "./sample_redaction/sample_output" |
| output_format | str | Defines the output file type. It must either be JSON or HTML. | JSON |
| model | str | The language model to use. | phi4 |
| prompt_type | str | Prompt to be passed to the LLM. (Options:: "default", "few_shot", "one_shot", "custom") | "default" |
| num_runs | int | The number of times to run the redaction on each file. | 1 |
| aggregation | str | If num_runs > 1, the aggregation method used to summarize the runs for each file. (Options: "restrictive", "threshold", "majority", "lenient") | "restrictive" |
| threshold | float | If aggregation type is "threshold", the threshold desired (i.e. 0.35, 0.75) | 0.5 |
| temperature | float | The temperature (creativity) of the model. | None, Ollama defaults to 0.8. |
| seed | int | The random number seed to use for generation. | None, Ollama defaults to a random value. |
| prompt_fp | str | If prompt_type is "custom", provide the path the the TXT file. | None |


For more details on optional arguments, please see [Ollama's official documentation](https://ollama.readthedocs.io/en/modelfile/#valid-parameters-and-values). To see if your model via Ollama has any different default options different from the official documentation, you can run:

```sh
ollama show --parameters YOUR-MODEL
```
See [redact_pii.py](./scripts/process/redact_pii.py) for the script's implementation and to adjust any keyword arguments.

### Usage Example
Assuming that your text files are in a folder called `sample_redaction/sample_input` and the folder `sample_redaction/sample_output` exists to store the redaction output, please see [sample_run.py](./scripts/sample_run.py)):
```py
"""
sample_run.py
example of running run_redaction() from app.redact_pii
"""
from process.redaction import run_redaction
from process.aggregate import run_aggregation

def main():
    """
    main entrypoint
    """
    ## Run aggregation redaction on unprocessed files
    for prompt in ['default', 'one_shot', 'few_shot']:
        ## Run aggregation redaction on unprocessed files
        kwargs = {"output_dir": "./sample_redaction/sample_output", "output_format": "json", "model": "phi4", "prompt_type": prompt,
                    "num_runs": 4, "aggregation": "majority"}
        run_redaction(["./sample_redaction/sample_input"], **kwargs)
        kwargs = {"output_dir": "./sample_redaction/sample_output", "output_format": "html", "model": "phi4", "prompt_type": prompt,
                    "num_runs": 4, "aggregation": "majority"}
        run_redaction(["./sample_redaction/sample_input"], **kwargs)

        ## Run aggregation redaction on previously processed files
        run_aggregation("json", f"./sample_redaction/sample_output/phi4/{prompt}", "lenient", None)
        run_aggregation("html", f"./sample_redaction/sample_output/phi4/{prompt}", "lenient", None)
        run_aggregation("json", f"./sample_redaction/sample_output/phi4/{prompt}", "restrictive", None)
        run_aggregation("html", f"./sample_redaction/sample_output/phi4/{prompt}", "restrictive", None)
        run_aggregation("json", f"./sample_redaction/sample_output/phi4/{prompt}", "threshold", 0.75)
        run_aggregation("html", f"./sample_redaction/sample_output/phi4/{prompt}", "threshold", 0.75)

if __name__ == '__main__':
    main()

```
See [Sample Input and Output Files](#sample-input-and-output-files) for more information on input and output files.

# Multiple Runs
This tool supports the option to run N times on the same text and aggregate the results with a specified threshold. The threshold options include:
| Name | Threshold value |
|--|--|
| restrictive | 0 |
| majority | 0.5 |
| lenient | 1 |
| threshold | user provided threshold |

If you would like to re-aggregate previous multiple runs using a different threshold value, see [scripts/run_aggregate](./scripts/run_aggregate.py). This takes in described above for running `main.py` using the CLI, allowing you to redefine which aggregation threshold to use. 
For instance, you could run:
```sh
cd scripts
 python run_aggregate.py --output_dir ../out/llama3.2/default --aggregation lenient
```

This assumes that `../out/llama3.2/default` holds files from a previous run where each file was processed more than once. 

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
docker run --gpus=all -v "$(dirname "$(pwd)"):/entry" -it --rm --name temp_pii_splicing pii_splicing
```

For more help, please see the official documentation [user tokens](https://huggingface.co/docs/hub/en/security-tokens) or the [Hugging Face CLI](https://huggingface.co/docs/huggingface_hub/en/guides/cli).

To evaluate the performance of this model, run the commands below in the root of the repo (python3 may be needed instead of python, depending on the environment):

```sh
mkdir data out
cd data
python ../scripts/evaluate/pii-masking-300k/export_pii_masking_300k.py
cd ..
cd scripts
python main.py --model llama3.2 ../data -o ../out
python scripts/evaluate/pii-masking-300k/pii_masking_evaluate.py
```

The default settings in [export_pii_masking_300k.py](scripts/pii-masking-300k/export_pii_masking_300k.py) will pull 10 files (see `set_size` in load_hugging_face_dataset()) from the `pii-masking-300k` dataset and write them to txt files in the data/ folder (0.txt, 1.txt, ...).

By default, [pii_masking_evaluate.py](scripts/pii-masking-300k/pii_masking_evaluate.py) will iterate over the contents `out/llama3.2/default` for JSON files (see `evaluate()`). A different model name can be supplied to pii_masking_evaluate.py to iterate over that directory instead.

```sh
python scripts/evaluate/pii-masking-300k/pii_masking_evaluate.py ## targets out/llama3.2/default
python scripts/evaluate/pii-masking-300k/pii_masking_evaluate.py --model llama3.2 ## targets out/llama3.2/default
python scripts/evaluate/pii-masking-300k/pii_masking_evaluate.py --model phi4 ## targets out/phi4/default
python scripts/evaluate/pii-masking-300k/pii_masking_evaluate.py --model phi4 --prompt_type one_shot ## targets out/phi4/one_shot
```

You many also evaluate aggregate results by supplying the aggregation name. If you chose to run multiple runs but want to evaluate a single run, use `one_run` as the value for the aggregation flag.
```sh
python scripts/evaluate/pii-masking-300k/pii_masking_evaluate.py --model phi4 --aggregation one_run ## targets the first file found in each subfolder of /out/phi4/default
python scripts/evaluate/pii-masking-300k/pii_masking_evaluate.py --model phi4 --aggregation majority ## targets majority files found in /out/phi4/default
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
   |   |-- default
   |   |   |-- llm_raw_response
   |   |   |   |-- 0-json.json
   |   |   |   |-- 1-json.json ## N-json.json for every input file
   |   |   |-- summaries
   |   |   |   |-- summary_YYYYMMDD_HHMMSS.json
   |   |   |   |-- summary_YYYYMMDD_HHMMSS.xlsx
   |   |   |-- 0.json
   |   |   |-- 1.json ## N.json for every input file

```
Further information on the structure of the output files can be seen in the [Sample Output Files](#sample-output-files) section.

The `out/llama3.2/default` directory will contain:
- The output JSON files (0.json, 1.json, ...9.json) from the PII redaction (same structure as [test_0.json](sample_redaction/sample_output/llama3.2/default/test_0.json)).
- A `llm_raw_response/` folder that contains the raw LLM response for each respective input file (same structure as [test-json_0.json](sample_redaction/sample_output/llama3.2/default/llm_raw_response/test-json_0.json)).
- A `summaries/` folder that contains:
    - A timestamped `summary_YYYY_MM_DD_HHMMSS.json` file that contains the performance metrics and other information. (see `write_summary_json()` in [pii_masking_evaluate.py](scripts/evaluate/pii-masking-300k/pii_masking_evaluate.py))
    - A timestamped `summary_YYYY_MM_DD_HHMMSS.xlsx` file that contains a Summary tab, and then individual tabs for each output JSON file that had no errors. (see `write_summary_xlsx()`in [pii_masking_evaluate.py](scripts/evalutate/pii-masking-300k/pii_masking_evaluate.py))

# Performance Metrics on pii-masking-300k
Results of the Phi4 and Llama3.2 LLM models on the first 500 rows of [pii-masking-300k](https://huggingface.co/datasets/ai4privacy/pii-masking-300k).

**Phi4 (Default Prompt)**

| Aggregation | Precision | Recall | F1 |
| -- | -- | -- | -- |
| one run | 91.8% | 84.6% | 88.1% |
| restrictive | 90.7% | 92.7% | 91.7% |
| majority | 92.1%| 83.7% | 87.7% |
| lenient | 91.2% | 71.8% | 80.3% |

**Phi4 (One Shot Prompt)**

| Aggregation | Precision | Recall | F1 |
| -- | -- | -- | -- |
| one run | 93.3% | 74.9% | 83.1% |
| restrictive | 90.7% | 92.7% | 91.7% |
| majority | 93.2%| 72.8% | 81.8% |
| lenient | 92.2% | 58.2% | 71.4% |

**Phi4 (Few Shot Prompt)**

| Aggregation | Precision | Recall | F1 |
| -- | -- | -- | -- |
| one run | 90.3% | 84.6% | 88.5% |
| restrictive | 89.6% | 94.0% | 91.7% |
| majority | 90.9% | 86.1% | 88.4% |
| lenient | 89.3% | 74.0% | 80.9% |


**Llama3.2 (Default Prompt)**

| Aggregation | Precision | Recall | F1 |
| -- | -- | -- | -- |
| one run | 91.8% | 84.6% | 88.1% |
| restrictive | 84.3% | 90.9% | 87.5% |
| majority | 91.0% | 70.2% | 79.3% |
| lenient | 86.1% | 54.0% | 66.4% |

**Llama3.2 (One Shot Prompt)**

| Aggregation | Precision | Recall | F1 |
| -- | -- | -- | -- |
| one run | 91.8% | 66.8% | 77.3% |
| restrictive | 89.6% | 94.0% | 91.7% |
| majority | 90.9% | 63.5% | 74.8% |
| lenient | 84.9% | 86.4% | 85.7% |

**Llama3.2 (Few Shot Prompt)**

| Aggregation | Precision | Recall | F1 |
| -- | -- | -- | -- |
| one run | 84.4% | 74.1% | 78.9% |
| restrictive | 74.2% | 90.1% | 81.4% |
| majority | 84.2% | 72.8% | 78.1% |
| lenient | 76.8% | 67.0% | 71.6% |

These results can be reproduced by running the [performance metric scripts](#calculate-performance-metrics-on-pii-masking-300k) and loading in the appropriate amount of data by adjusting the `set_size` to 500 in [export_pii_masking_300k.py](scripts/evaluate/pii-masking-300k/export_pii_masking_300k.py). Note that these results were generated without setting the seed or the temperature, so results will vary, even though the input data are the same. There were N=31 predicted words that were non-matches (not in the original text).

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