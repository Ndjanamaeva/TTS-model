import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from .schemas import TTSRequest, APIResponse
from .tts_service import synthesize_speech
from .utils import enforce_min_duration
import os

os.makedirs("downloads", exist_ok=True)
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

app = FastAPI(title="Kokoro TTS API")
@app.post("/tts", response_model=APIResponse)
def tts_endpoint(payload: TTSRequest):
    try:
        logging.info(f"TTS request received | text_length={len(payload.text)}")

        enforce_min_duration(payload.text)

        audio_path, duration, request_id = synthesize_speech(
            payload.text, payload.voice
        )

        return APIResponse(
            success=True,
            message="Audio generated successfully",
            data={
                "audio_url": f"/download/{request_id}",
                "duration_seconds": round(duration, 2)
            },
            request_id=request_id
        )

    except Exception as e:
        logging.error(f"TTS error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal TTS processing error"
        )
@app.get("/download/{request_id}")
def download_audio(request_id: str):
    file_path = f"downloads/tts_{request_id}.wav"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio not found")

    return FileResponse(
        file_path,
        media_type="audio/wav",
        filename="tts.wav"
    )
