import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

# Set page config
st.set_page_config(
    page_title="Liquid AI Chatbot",
    page_icon="💧",
    layout="wide"
)

MODEL_NAME = "LiquidAI/LFM2.5-1.2B-Instruct"

@st.cache_resource
def load_model():
    """Load the Liquid AI model with caching to avoid reloading"""
    with st.spinner("Loading Liquid AI model... This may take a few minutes on first run."):
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

def detect_question_type(prompt: str) -> str:
    """Detect the type of question to choose appropriate system prompt"""
    prompt_lower = prompt.lower()

    # Coding-related keywords
    coding_keywords = [
        'code', 'python', 'javascript', 'java', 'function', 'class', 'algorithm',
        'programming', 'script', 'method', 'variable', 'loop', 'if', 'else',
        'import', 'def', 'return', 'print', 'list', 'dictionary', 'array',
        'write a program', 'write code', 'implement', 'create a function',
        'debug', 'fix this code', 'syntax error', 'programming problem'
    ]

    # Math-related keywords
    math_keywords = [
        'equation', 'solve', 'calculate', 'mathematics', 'algebra', 'geometry',
        'calculus', 'trigonometry', 'statistics', 'probability', 'formula',
        'theorem', 'proof', 'derivative', 'integral', 'matrix', 'vector',
        'pythagorean', 'quadratic', 'linear', 'polynomial'
    ]

    # Science-related keywords
    science_keywords = [
        'physics', 'chemistry', 'biology', 'science', 'experiment', 'theory',
        'molecular', 'atom', 'electron', 'photosynthesis', 'gravity', 'energy',
        'reaction', 'DNA', 'cell', 'organism', 'hypothesis', 'scientific method'
    ]

    # Check for coding
    if any(keyword in prompt_lower for keyword in coding_keywords):
        return 'coding'

    # Check for math
    elif any(keyword in prompt_lower for keyword in math_keywords):
        return 'math'

    # Check for science
    elif any(keyword in prompt_lower for keyword in science_keywords):
        return 'science'

    # Default to general
    else:
        return 'general'

def get_system_prompt(question_type: str, user_prompt: str) -> str:
    """Get appropriate system prompt based on question type"""

    if question_type == 'coding':
        return (
            "You are a helpful programming assistant.\n"
            "Write clean, well-formatted, well-commented code and explain it clearly.\n"
            "Provide working examples and explain the logic step by step.\n\n"
            f"Programming task:\n{user_prompt}\n\nSolution with explanation:\n"
        )

    elif question_type == 'math':
        return (
            "You are a patient math tutor.\n"
            "Solve problems step by step, showing all work clearly.\n"
            "Explain each step and the reasoning behind it.\n\n"
            f"Math problem:\n{user_prompt}\n\nStep-by-step solution:\n"
        )

    elif question_type == 'science':
        return (
            "You are a knowledgeable science teacher.\n"
            "Explain scientific concepts clearly with examples and analogies.\n"
            "Break down complex topics into understandable parts.\n\n"
            f"Science question:\n{user_prompt}\n\nExplanation:\n"
        )

    else:  # general
        return (
            "You are a friendly teacher.\n"
            "Explain your answer step by step in simple language.\n\n"
            f"Question:\n{user_prompt}\n\nAnswer:\n"
        )

def generate_response(prompt: str, max_new_tokens: int = 256, temperature: float = 0.4, top_p: float = 0.9) -> tuple[str, str]:
    """Generate response from the model with smart prompt selection"""
    tokenizer, model = load_model()

    # Detect question type and get appropriate system prompt
    question_type = detect_question_type(prompt)
    full_prompt = get_system_prompt(question_type, prompt)

    inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Return the response and question type
    response = text[len(full_prompt):].strip()
    return response, question_type

def get_prompt_type_emoji(question_type: str) -> str:
    """Get emoji for question type"""
    type_emojis = {
        'coding': '💻',
        'math': '🔢',
        'science': '🔬',
        'general': '💬'
    }
    return type_emojis.get(question_type, '💬')

def main():
    st.title("💧 Liquid AI Chatbot")
    st.subheader("Powered by LFM2.5-1.2B-Instruct Model")

    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Model Settings")

        max_tokens = st.slider(
            "Max Response Length",
            min_value=50,
            max_value=1024,
            value=256,
            step=50,
            help="Maximum number of tokens in the response"
        )

        temperature = st.slider(
            "Temperature",
            min_value=0.1,
            max_value=1.0,
            value=0.4,
            step=0.1,
            help="Controls randomness: lower = more focused, higher = more creative"
        )

        top_p = st.slider(
            "Top P (Nucleus Sampling)",
            min_value=0.1,
            max_value=1.0,
            value=0.9,
            step=0.1,
            help="Controls diversity by probability mass: lower = more focused"
        )

        st.divider()

        # Add prompt type indicator
        st.header("🎯 Smart Prompts")
        st.write("The app automatically detects question type and uses optimized prompts:")
        st.write("• 💻 **Coding**: Programming assistant")
        st.write("• 🔢 **Math**: Step-by-step math tutor")
        st.write("• 🔬 **Science**: Science teacher with examples")
        st.write("• 💬 **General**: Friendly teacher")

        st.divider()

        st.header("About")
        st.write("""
        This chatbot uses Liquid AI's LFM2.5-1.2B-Instruct model,
        a compact and efficient language model designed for educational
        content and step-by-step explanations.

        **Best for:**
        - Math problems
        - Science explanations
        - Coding questions
        - Step-by-step tutorials
        """)

        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask me anything about math, science, or coding..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response, question_type = generate_response(prompt, max_tokens, temperature, top_p)

                # Show prompt type indicator
                prompt_emoji = get_prompt_type_emoji(question_type)
                st.markdown(f"*{prompt_emoji} Detected: {question_type.title()} mode*")

                st.markdown(response)

                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"*{prompt_emoji} Detected: {question_type.title()} mode*\n\n{response}"
                })

    # Example questions
    if len(st.session_state.messages) == 0:
        st.markdown("### 🚀 Try these example questions to see smart prompts in action:")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("💻 Write a Python function to calculate fibonacci"):
                st.session_state.example_prompt = "Write a Python function to calculate the nth fibonacci number"
                st.rerun()

            if st.button("📐 Solve quadratic equation"):
                st.session_state.example_prompt = "Solve the quadratic equation: x² - 5x + 6 = 0"
                st.rerun()

            if st.button("🔬 Explain photosynthesis"):
                st.session_state.example_prompt = "Explain how photosynthesis works in plants"
                st.rerun()

        with col2:
            if st.button("🔵 Why is the sky blue?"):
                st.session_state.example_prompt = "Why is the sky blue?"
                st.rerun()

            if st.button("🐍 Create a class in Python"):
                st.session_state.example_prompt = "Create a Python class for a simple calculator with add, subtract, multiply, and divide methods"
                st.rerun()

            if st.button("⚡ Speed vs velocity difference"):
                st.session_state.example_prompt = "What is the difference between speed and velocity? Give examples."
                st.rerun()

        # Handle example prompts
        if hasattr(st.session_state, 'example_prompt'):
            prompt = st.session_state.example_prompt
            del st.session_state.example_prompt

            # Add to chat history and generate response
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.spinner("Thinking..."):
                response, question_type = generate_response(prompt, max_tokens, temperature, top_p)
                prompt_emoji = get_prompt_type_emoji(question_type)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"*{prompt_emoji} Detected: {question_type.title()} mode*\n\n{response}"
                })

            st.rerun()

if __name__ == "__main__":
    main()