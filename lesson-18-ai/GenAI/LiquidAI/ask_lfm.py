from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

MODEL_NAME = "LiquidAI/LFM2.5-1.2B-Instruct"
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    
    # Define a BitsAndBytesConfig for 4-bit quantization
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",  # or "fp4"
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto",      # automatically uses GPU if available
        quantization_config=bnb_config       # Use the new quantization_config
    )
    return tokenizer, model

def ask_lfm25(prompt: str, max_new_tokens: int = 256) -> str:
    tokenizer, model = load_model()
    # Wrap the user prompt in a simple instruction pattern
    prompt = (
        "You are a friendly teacher.\n"
        "Explain your answer step by step in simple language.\n\n"
        f"Question:\n{prompt}\n\nAnswer:\n"
    )
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.4,   # low temp = more stable, focused answers
            top_p=0.9,
            do_sample=True
        )
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Return only the part after our prompt
    return text[len(prompt):].strip()


def generate_code(task: str, max_new_tokens: int = 256) -> str:
    tokenizer, model = load_model()
    prompt = (
        "You are a careful Python assistant.\n"
        "Write clean, well-formatted, well-commented code and then briefly explain it.\n\n"
        f"Task:\n{task}\n\nPython solution with comments and short explanation:\n"
    )
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.35,
            top_p=0.9,
            do_sample=True
        )
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text[len(prompt):].strip()


if __name__ == "__main__":
    q = "Why is the sky blue?"
    print(ask_lfm25(q))