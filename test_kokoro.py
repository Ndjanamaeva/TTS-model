import torch
import soundfile as sf
from kokoro import KPipeline

# Create pipeline for English (American English - 'a')
# This will automatically download and load the model
pipeline = KPipeline(lang_code='a', device='cpu')

# Text to synthesize
text = "Hello! This is a test of the Kokoro text to speech model."

# Use a local voice file (adult female)
voice = "voices/af.pt"

# Run inference - returns a generator of Result objects
# Collect all audio chunks
audio_chunks = []
for result in pipeline(text, voice=voice):
    if result.output and result.audio is not None:
        audio_chunks.append(result.audio)

# Concatenate audio chunks
if audio_chunks:
    audio = torch.cat(audio_chunks, dim=-1).numpy()
    sample_rate = 24000  # Kokoro uses 24kHz
    
    # Save output
    sf.write("output.wav", audio, sample_rate)
    print("✅ Audio saved as output.wav")
else:
    print("❌ No audio generated")
