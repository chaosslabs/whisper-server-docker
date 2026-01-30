import os
import tempfile
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from faster_whisper import WhisperModel

app = FastAPI(title="Whisper Transcription Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")


@app.post("/v1/audio/transcriptions")
async def transcribe_audio(
    file: UploadFile = File(...),
    model_name: str = Form(default=None, alias="model"),
):
    """
    OpenAI-compatible transcription endpoint.
    Accepts audio files and returns transcribed text.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    # Get file extension from original filename
    suffix = os.path.splitext(file.filename)[1] if file.filename else ".wav"

    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        segments, _ = model.transcribe(tmp_path)
        text = "".join(segment.text for segment in segments).strip()
        return JSONResponse(content={"text": text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


def main():
    import uvicorn
    host = os.environ.get("WHISPER_SERVER_HOST", "0.0.0.0")
    port = int(os.environ.get("WHISPER_SERVER_PORT", "8080"))
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
