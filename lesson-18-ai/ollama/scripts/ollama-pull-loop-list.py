import subprocess

# List of models and their sizes
models = """
llama3.1:8b
gemma2:9b
qwen2.5:7b
phi3.5:3.8b
nemotron-mini:4b
mistral:7b
codegemma:7b
"""

# Loop through the models
for line in models.strip().split('\n'):
    if not line.strip(): continue  # Skip empty lines

    name, size = line.split(':')
    print(f"Pulling model: {name} ({size})")
    
    # Run the ollama pull command
    try:
        subprocess.run(["ollama", "pull", name.strip()], check=True)
        print("Pull successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error pulling model {name}: {e}")
    except FileNotFoundError:
        print("Error: 'ollama' command not found. Make sure it's installed and in your PATH.")
    
    # Print a blank line for better readability
    print()