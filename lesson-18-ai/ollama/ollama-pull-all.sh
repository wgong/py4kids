ollama_models=$(ollama list | awk '{print $1}' )  # Capture output in a variable
for model in $ollama_models; do
  ollama pull "$model"  # Loop through each model name and call pull
done
