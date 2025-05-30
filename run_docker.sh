#!/bin/bash

# Default values
CONTAINER_NAME="pii_splicing_container"
IMAGE_NAME="pii_splicing"
MODEL_VERSION="llama3.2"
OUTPUT_FORMAT="json"
SEED=0
TEMP=0.8
INPUT_FILE="sample_input"
HOST_DIR="./sample_redaction"
CONTAINER_DIR="/data"

# Parse command-line arguments if included
while [[ $# -gt 0 ]]; do
  case $1 in
    --container-name)
      CONTAINER_NAME="$2"
      shift 2
      ;;
    --image-name)
      IMAGE_NAME="$2"
      shift 2
      ;;
    --model)
      MODEL_VERSION="$2"
      shift 2
      ;;
    --output_format)
      OUTPUT_FORMAT="$2"
      shift 2
      ;;
    --seed)
      SEED="$2"
      shift 2
      ;;
    --temperature)
      TEMP="$2"
      shift 2
      ;;
    --input)
      INPUT_FILE="$2"
      shift 2
      ;;
    --host-dir)
      HOST_DIR="$2"
      shift 2
      ;;
    --container-dir)
      CONTAINER_DIR="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

HOST_DIR_ABS=$(realpath "$HOST_DIR")

docker run -v "$HOST_DIR_ABS":"$CONTAINER_DIR" -it --rm --name "$CONTAINER_NAME" "$IMAGE_NAME" --model "$MODEL_VERSION" --output_format "$OUTPUT_FORMAT" --seed "$SEED" --temperature "$TEMP" "$CONTAINER_DIR/$INPUT_FILE"
