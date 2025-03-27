#!/bin/sh

ollama serve 2>&1 > /dev/null &
python3 /app/main.py "$@"
