#!/bin/bash

# Start Ollama server in background
ollama serve & 2>&1 > /dev/null &

# # Wait until ready
until ollama list > /dev/null 2>&1; do
  sleep 1
done

# Change to mounted directory
cd /entry || exit 1

# If no args, open interactive shell
if [ "$#" -eq 0 ]; then
    exec /bin/bash
else
    # Run the command
    "$@"
    
    # Optionally drop into Bash after the command finishes
    exec /bin/bash
fi