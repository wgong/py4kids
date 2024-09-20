#!/bin/sh

# List-like structure of model names and their sizes
models="
llama3.1:8b
gemma2:9b
qwen2.5:7b
phi3.5:3.8b
nemotron-mini:4b
mistral:7b
codegemma:7b
"

# Loop through the models
echo "$models" | while IFS=':' read -r name size; do
    # Skip empty lines
    [ -z "$name" ] && continue
    
    # Print the model name and size
    echo "Pulling model: $name ($size)"
    
    # Run the ollama pull command
    ollama pull "$name"
    
    # Print a blank line for better readability
    echo
done