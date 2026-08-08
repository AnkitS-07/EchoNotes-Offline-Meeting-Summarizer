# 🎙️ Local Meeting Summarizer

A fully offline, full-stack app that turns any meeting/lecture recording into
structured notes — no cloud APIs, no API keys, everything runs on your machine.

**Pipeline:** Audio → local Whisper transcription → local LLM (Ollama) →
structured summary, decisions, and action items → saved to SQLite.

## Tech Stack

- **Backend:** FastAPI (Python)
- **Transcription:** faster-whisper (runs on CPU, no internet needed)
- **Summarization:** Ollama running a small local model (e.g. Llama 3.2 3B)
- **Database:** SQLite (plain sqlite3, no ORM)
- **Frontend:** Vanilla HTML/CSS/JS (no build tools required)

## Setup

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Ollama and pull a model
Download Ollama from https://ollama.com, then run:
```bash
ollama pull llama3.2:3b
```
Make sure Ollama is running in the background (it usually starts automatically).

### 3. Run the app
```bash
uvicorn app.main:app --reload
```

### 4. Open in browser
Go to http://localhost:8000

## How to Use

1. Go to the **New Meeting** tab
2. Upload an audio file (mp3, wav, m4a, etc.)
3. Click **Transcribe & Summarize** — this runs locally and may take
   a minute depending on audio length and your machine
4. View the summary, key decisions, and action items
5. Check the **History** tab to revisit past meetings

## Project Structure

```
meeting-summarizer/
├── app/
│   ├── main.py          # FastAPI routes
│   ├── transcriber.py    # faster-whisper wrapper
│   ├── summarizer.py     # Ollama wrapper + prompt
│   └── database.py       # SQLite storage
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── uploads/               # uploaded audio files (created at runtime)
├── data/                  # SQLite database (created at runtime)
├── requirements.txt
└── README.md
```

## Notes for Customization

- Swap the Whisper model size in `transcriber.py` (`tiny`/`base`/`small`/`medium`/`large-v3`)
  for a speed/accuracy tradeoff.
- Swap the Ollama model in `summarizer.py` (`MODEL_NAME`) for any model
  you've pulled locally.
- The LLM is prompted to return strict JSON — if you want richer notes
  (e.g. attendee list, topics discussed), just extend the prompt template
  and the JSON schema in `summarizer.py`.
