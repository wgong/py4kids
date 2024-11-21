using qwen2.5-coder for text2sql use-case test,
it achieved 4 sec/question after a reboot.
I see Ollama is loaded in nvidia-smi

Suspect ubuntu overnite, re-test in the morning,
ollama is off-loaded from GPU, a question took 60-110 sec
That means Ollama is using CPU

see screenshots in ~/Pictures/Ollama

Enable GPU for Ollama by setting options={"gpu": True}

CPU results

Completed testing:
================
 LLM model 'qwen2.5-coder' 
 took 4886 sec
 run on 'papa-game' 
 at 20241120-084734