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
wav, sr = torchaudio.load("assets/question.wav")   # your recorded question
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