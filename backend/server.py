from datetime import datetime
from pathlib import Path
import shutil
import tempfile
import wave

import numpy as np
import sounddevice as sd

from fastapi import FastAPI, File, HTTPException, UploadFile
from faster_whisper import WhisperModel


app = FastAPI(
    title="NOVA Backend",
    description="Local backend for NOVA — personal AI assistant for Windows.",
    version="0.2.0",
)


# =========================
# WHISPER CONFIGURATION
# =========================

MODEL_SIZE = "base"
SAMPLE_RATE = 16000
CHANNELS = 1
RECORD_SECONDS = 5

model = WhisperModel(
    MODEL_SIZE,
    device="cpu",
    compute_type="int8",
)


# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "assistant": "Nova",
        "time": datetime.now().isoformat(),
    }


@app.get("/")
def root():
    return {
        "message": "Nova backend is running."
    }


# =========================
# SPEECH TRANSCRIPTION
# =========================

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No audio file provided.",
        )

    temporary_path = None

    try:
        suffix = Path(file.filename).suffix or ".wav"

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            temporary_path = Path(temp_file.name)

            shutil.copyfileobj(
                file.file,
                temp_file,
            )

        segments, info = model.transcribe(
            str(temporary_path),
            language="en",
            beam_size=5,
        )

        text_parts = []

        for segment in segments:
            text = segment.text.strip()

            if text:
                text_parts.append(text)

        text = " ".join(text_parts)

        return {
            "text": text,
            "language": info.language,
            "language_probability": info.language_probability,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {error}",
        )

    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()
@app.post("/listen")
def listen():
    temporary_path = None

    try:
        print("Listening...")

        recording = sd.rec(
            int(RECORD_SECONDS * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16",
        )

        sd.wait()

        print("Recording finished.")

        audio = np.asarray(recording, dtype=np.int16)

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav",
        ) as temp_file:
            temporary_path = Path(temp_file.name)

        with wave.open(str(temporary_path), "wb") as wav_file:
            wav_file.setnchannels(CHANNELS)
            wav_file.setsampwidth(2)
            wav_file.setframerate(SAMPLE_RATE)
            wav_file.writeframes(audio.tobytes())

        segments, info = model.transcribe(
            str(temporary_path),
            language="en",
            beam_size=5,
        )

        text_parts = []

        for segment in segments:
            text = segment.text.strip()

            if text:
                text_parts.append(text)

        text = " ".join(text_parts)

        return {
            "text": text,
            "language": info.language,
            "language_probability": info.language_probability,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Listening failed: {error}",
        )

    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()           