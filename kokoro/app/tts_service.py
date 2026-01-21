import uuid
import soundfile as sf
from kokoro import KPipeline

# Load model ONCE (important for performance)
# Using American English pipeline with default Kokoro-82M model
pipeline = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M')

SAMPLE_RATE = 24000

def synthesize_speech(text: str, voice: str):
    # Remove .pt extension if present for voice name
    voice_name = voice.replace('.pt', '') if voice.endswith('.pt') else voice

    # Generate audio using the pipeline
    audio_chunks = []
    for result in pipeline(text, voice=voice_name):
        if result.audio is not None:
            audio_chunks.append(result.audio.numpy())

    # Concatenate all audio chunks
    import numpy as np
    audio = np.concatenate(audio_chunks) if audio_chunks else np.array([])

    request_id = str(uuid.uuid4())
    output_path = f"downloads/tts_{request_id}.wav"

    sf.write(output_path, audio, SAMPLE_RATE)

    duration = len(audio) / SAMPLE_RATE

    return output_path, duration, request_id
