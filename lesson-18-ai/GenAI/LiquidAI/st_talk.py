import streamlit as st
import torch
import torchaudio
import tempfile
import os
from pathlib import Path
import numpy as np

try:
    from liquid_audio import (
        LFM2AudioModel,
        LFM2AudioProcessor,
        ChatState,
        LFMModality,
    )
    LIQUID_AUDIO_AVAILABLE = True
except ImportError:
    LIQUID_AUDIO_AVAILABLE = False
    st.error("liquid_audio package not found. Please install it to use audio features.")

# Set page config
st.set_page_config(
    page_title="Liquid AI Audio Chat",
    page_icon="🎙️",
    layout="wide"
)

# HuggingFace model repository
HF_REPO = "LiquidAI/LFM2.5-Audio-1.5B"

@st.cache_resource
def load_audio_model():
    """Load the Liquid AI audio model with caching"""
    if not LIQUID_AUDIO_AVAILABLE:
        return None, None

    with st.spinner("Loading Liquid AI Audio model... This may take several minutes on first run."):
        try:
            processor = LFM2AudioProcessor.from_pretrained(HF_REPO).eval()
            model = LFM2AudioModel.from_pretrained(HF_REPO).eval()
            return processor, model
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            return None, None

def create_chat_state(processor):
    """Create a new chat state"""
    if processor is None:
        return None
    return ChatState(processor)

def process_audio_conversation(chat, model, processor, user_audio_path, system_message="Respond with interleaved text and audio."):
    """Process audio conversation using LFM2.5-Audio model"""
    try:
        # System message: tell the model how to behave
        chat.new_turn("system")
        chat.add_text(system_message)
        chat.end_turn()

        # User turn: audio question
        chat.new_turn("user")
        wav, sr = torchaudio.load(user_audio_path)
        chat.add_audio(wav, sr)
        chat.end_turn()

        # Assistant turn: generate mixed text + audio
        chat.new_turn("assistant")
        text_out = []
        audio_out = []
        modalities = []

        response_text = ""

        for t in model.generate_interleaved(
            **chat,
            max_new_tokens=512,
            audio_temperature=1.0,
            audio_top_k=4
        ):
            # Single-token tensors represent text tokens
            if t.numel() == 1:
                token_text = processor.text.decode(t)
                response_text += token_text
                text_out.append(t)
                modalities.append(LFMModality.TEXT)
            else:
                # Longer tensors represent audio codes
                audio_out.append(t)
                modalities.append(LFMModality.AUDIO_OUT)

        # Turn the generated audio codes into a waveform
        if len(audio_out) > 1:
            audio_codes = torch.stack(audio_out[:-1], 1).unsqueeze(0)
            waveform = processor.decode(audio_codes)

            # Save the generated audio
            output_path = tempfile.mktemp(suffix=".wav")
            torchaudio.save(output_path, waveform.cpu(), 24_000)

            return response_text, output_path
        else:
            return response_text, None

    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
        return None, None

def save_uploaded_audio(uploaded_file):
    """Save uploaded audio file to temporary location"""
    if uploaded_file is not None:
        temp_path = tempfile.mktemp(suffix=".wav")
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        return temp_path
    return None

def main():
    st.title("🎙️ Liquid AI Audio Chat")
    st.subheader("Powered by LFM2.5-Audio-1.5B Model")

    if not LIQUID_AUDIO_AVAILABLE:
        st.error("⚠️ liquid_audio package is not available. Please install the required dependencies.")
        st.code("""
        # Install liquid_audio package
        pip install liquid-audio
        # Or follow Liquid AI's installation instructions
        """)
        return

    # Load model
    processor, model = load_audio_model()

    if processor is None or model is None:
        st.error("Failed to load the audio model. Please check your installation and model availability.")
        return

    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Audio Settings")

        system_message = st.text_area(
            "System Message",
            value="You are a helpful language learning assistant. Respond with clear speech and helpful explanations.",
            height=100,
            help="Instruction for how the AI should behave"
        )

        st.divider()

        st.header("🎯 Language Learning Mode")
        learning_modes = {
            "General Conversation": "You are a helpful assistant. Respond with interleaved text and audio.",
            "Chinese Tutor": "You are a patient Chinese language tutor. Speak clearly in Mandarin, correct pronunciation gently, and explain step by step. Respond with interleaved text and audio.",
            "English Practice": "You are an English conversation partner. Help improve pronunciation and fluency. Respond with interleaved text and audio.",
            "Pronunciation Coach": "You are a pronunciation coach. Listen carefully and provide detailed feedback on pronunciation. Respond with interleaved text and audio."
        }

        selected_mode = st.selectbox("Select Learning Mode:", list(learning_modes.keys()))
        system_message = learning_modes[selected_mode]

        st.divider()

        st.header("📖 About")
        st.write("""
        This app uses Liquid AI's LFM2.5-Audio-1.5B model for
        native audio processing. Features:

        - **Real-time audio conversation**
        - **Native audio processing** (not pipelined)
        - **On-device inference**
        - **Multilingual support**
        - **Educational applications**
        """)

    # Initialize chat state in session state
    if "chat_state" not in st.session_state:
        st.session_state.chat_state = create_chat_state(processor)

    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    # Main interface
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("🎤 Audio Input")

        # Audio upload
        uploaded_audio = st.file_uploader(
            "Upload Audio File",
            type=['wav', 'mp3', 'flac', 'm4a'],
            help="Upload an audio file to have a conversation"
        )

        # Audio recording (placeholder - requires additional setup)
        st.info("🔍 **Note**: For live recording, you'll need to set up audio recording capabilities in your environment.")

        # Sample questions
        st.subheader("🎯 Try These Sample Questions")
        sample_questions = [
            "Hello, how are you today?",
            "Can you help me practice Chinese pronunciation?",
            "What's the weather like?",
            "Tell me a short story.",
            "Help me learn new vocabulary."
        ]

        for question in sample_questions:
            if st.button(f"🔊 {question}", key=f"sample_{question}"):
                st.session_state.selected_sample = question
                # Note: In a real implementation, you'd convert text to speech for testing
                st.info(f"Selected: {question}")

        # Process audio button
        if uploaded_audio is not None:
            st.audio(uploaded_audio, format='audio/wav')

            if st.button("🎯 Process Audio", type="primary"):
                with st.spinner("Processing your audio..."):
                    # Save uploaded audio
                    audio_path = save_uploaded_audio(uploaded_audio)

                    if audio_path:
                        # Create new chat state for this conversation
                        chat = create_chat_state(processor)

                        # Process the conversation
                        response_text, response_audio_path = process_audio_conversation(
                            chat, model, processor, audio_path, system_message
                        )

                        if response_text:
                            # Store in conversation history
                            st.session_state.conversation_history.append({
                                "type": "user_audio",
                                "content": "Audio message",
                                "file_path": audio_path
                            })
                            st.session_state.conversation_history.append({
                                "type": "assistant",
                                "content": response_text,
                                "audio_path": response_audio_path
                            })

                        # Clean up temporary file
                        try:
                            os.unlink(audio_path)
                        except:
                            pass

    with col2:
        st.header("🤖 AI Response")

        # Display conversation history
        if st.session_state.conversation_history:
            for i, message in enumerate(st.session_state.conversation_history):
                if message["type"] == "user_audio":
                    st.write("👤 **You** (Audio):")
                    if os.path.exists(message.get("file_path", "")):
                        st.audio(message["file_path"], format='audio/wav')
                    else:
                        st.write("🎵 Audio message")

                elif message["type"] == "assistant":
                    st.write("🤖 **Assistant**:")
                    st.write(message["content"])

                    if message.get("audio_path") and os.path.exists(message["audio_path"]):
                        st.audio(message["audio_path"], format='audio/wav')
                        st.write("🎵 Generated Audio Response")

                st.divider()
        else:
            st.info("👆 Upload an audio file and click 'Process Audio' to start the conversation!")

    # Clear conversation button
    if st.button("🗑️ Clear Conversation"):
        st.session_state.conversation_history = []
        st.session_state.chat_state = create_chat_state(processor)
        st.rerun()

    # Advanced features
    with st.expander("🔧 Advanced Features & Code"):
        st.subheader("Model Architecture")
        st.write("""
        The LFM2.5-Audio-1.5B model uses Liquid AI's hybrid architecture:
        - Native audio processing (no pipeline)
        - Real-time conversation capabilities
        - <1GB RAM usage on mobile devices
        - 8x faster than previous LFM2 audio model
        """)

        st.subheader("Core Implementation")
        st.code('''
import torch
import torchaudio
from liquid_audio import (
    LFM2AudioModel,
    LFM2AudioProcessor,
    ChatState,
    LFMModality,
)

HF_REPO = "LiquidAI/LFM2.5-Audio-1.5B"

# Load processor and model
processor = LFM2AudioProcessor.from_pretrained(HF_REPO).eval()
model = LFM2AudioModel.from_pretrained(HF_REPO).eval()

# Create a chat state to hold the conversation
chat = ChatState(processor)

# System message: tell the model how to behave
chat.new_turn("system")
chat.add_text("Respond with interleaved text and audio.")
chat.end_turn()

# First user turn: audio question
chat.new_turn("user")
wav, sr = torchaudio.load("assets/question.wav")
chat.add_audio(wav, sr)
chat.end_turn()

# Assistant turn: generate mixed text + audio
chat.new_turn("assistant")
text_out = []
audio_out = []
modalities = []

for t in model.generate_interleaved(
    **chat,
    max_new_tokens=512,
    audio_temperature=1.0,
    audio_top_k=4
):
    # Single-token tensors represent text tokens
    if t.numel() == 1:
        print(processor.text.decode(t), end="", flush=True)
        text_out.append(t)
        modalities.append(LFMModality.TEXT)
    else:
        # Longer tensors represent audio codes
        audio_out.append(t)
        modalities.append(LFMModality.AUDIO_OUT)

# Turn the generated audio codes into a waveform
audio_codes = torch.stack(audio_out[:-1], 1).unsqueeze(0)
waveform = processor.decode(audio_codes)
torchaudio.save("answer1.wav", waveform.cpu(), 24_000)
        ''', language='python')

if __name__ == "__main__":
    main()