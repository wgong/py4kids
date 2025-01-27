#!/bin/bash

# list_ollama: Lists Ollama models sorted alphabetically by name.
# This script uses 'ollama list', removes the header row, and then sorts by the first column.

if ! command -v ollama &> /dev/null
then
    echo "Error: ollama command not found."
    exit 1
fi

ollama list | tail -n +2 | sort -k1,1
