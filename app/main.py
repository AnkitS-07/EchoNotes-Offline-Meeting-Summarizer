"""
Local Meeting Summarizer - Main FastAPI App
--------------------------------------------
Everything runs on your machine. No API keys, no cloud calls.

Flow:
1. User uploads/records an audio file from the browser
2. faster-whisper transcribes it locally
3. Ollama (local LLM) turns the transcript into structured notes
4. Everything is saved to a local SQLite database
"""

from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import shutil
import os

from app import database, transcriber, summarizer

app = FastAPI(title="Local Meeting Summarizer")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Create the database tables on startup
database.init_db()

# Serve the frontend (index.html, style.css, script.js)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def serve_home():
    return FileResponse("static/index.html")


@app.post("/api/process")
async def process_audio(file: UploadFile = File(...)):
    """
    Takes an uploaded audio file, transcribes it, summarizes it,
    saves it, and returns the structured notes.
    """
    # 1. Save the uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Transcribe locally with faster-whisper
    transcript = transcriber.transcribe(file_path)

    # 3. Summarize locally with Ollama
    notes = summarizer.generate_notes(transcript)

    # 4. Save everything to SQLite
    meeting_id = database.save_meeting(
        filename=file.filename,
        transcript=transcript,
        summary=notes["summary"],
        decisions=notes["decisions"],
        action_items=notes["action_items"],
    )

    return {
        "id": meeting_id,
        "transcript": transcript,
        "notes": notes,
    }


@app.get("/api/meetings")
def list_meetings():
    """Returns all past meetings (for the History tab)."""
    return database.get_all_meetings()


@app.get("/api/meetings/{meeting_id}")
def get_meeting(meeting_id: int):
    """Returns one meeting's full details."""
    return database.get_meeting(meeting_id)
