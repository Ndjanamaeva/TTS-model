from pydantic import BaseModel, Field

class TTSRequest(BaseModel):
    text: str = Field(..., min_length=5, max_length=500)
    voice: str = Field(default="af_heart")

class APIResponse(BaseModel):
    success: bool
    message: str
    data: dict | None
    request_id: str
