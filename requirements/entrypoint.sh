#!/bin/bash

# Start Ollama server in background
ollama serve & 2>&1 > /dev/null &

# Wait for server to be up (you could improve this)
sleep 5

# If no args, open interactive shell
if [ "$#" -eq 0 ]; then
    exec /bin/bash
else
    # Run the command
    "$@"
    
    # Optionally drop into Bash after the command finishes
    exec /bin/bash
fi