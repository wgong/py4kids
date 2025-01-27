import subprocess

def parse_model(line):
    # pickup model name
    model_name = ""
    parts = [i.strip() for i in line.split() if i.strip()]
    if not parts:
        return model_name
        
    model = parts[0]
    if model.endswith(':latest'):
        # Remove :latest suffix
        model_name = model[:-len(':latest')]
    else:
        model_name = model

    if model_name.endswith(':latest'):
        model_name = model_name.replace(':latest', '')
    return model_name

file_txt = "list_ollama.txt"
# Sample content (replace with your actual input method)
content = open(file_txt).read()

# Process content and collect unique models
models_to_pull = set()
models_to_rm = set()

for line in content.split('\n'):
    line = line.strip()
    if not line or line.startswith('(base)'):
        continue
    
    # remove model if startswith #
    if line.startswith('#'):
        model_name = parse_model(line.replace("#", ""))
        models_to_rm.add(model_name)
        continue

    model_name = parse_model(line)
    models_to_pull.add(model_name)


b_dry_run = False # True # 
if b_dry_run:
    print("Models to pull:\n", models_to_pull)
    print("Models to remove:\n", models_to_rm)
else:
    # Execute ollama pull commands
    for model in models_to_pull:
        print(f"Pulling {model}...")
        subprocess.run(['ollama', 'pull', model], check=True)
        print(f"Successfully pulled {model}\n")

    # remove models
    for model in models_to_rm:
        print(f"Removing {model}...")
        subprocess.run(['ollama', 'rm', model], check=True)
        print(f"Successfully removed {model}\n")

