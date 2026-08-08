"""
Summarizer module - talks to a locally running Ollama model
to turn a raw transcript into structured meeting notes.

Requires Ollama installed and running locally (https://ollama.com)
Pull a small model first, e.g.:
    ollama pull llama3.2:3b
"""

import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"  # swap for any local model you have pulled

PROMPT_TEMPLATE = """You are a meeting notes assistant.
Read the transcript below and respond with ONLY valid JSON
in exactly this format, nothing else:

{{
  "summary": "2-3 sentence summary of the meeting",
  "decisions": ["decision 1", "decision 2"],
  "action_items": ["action item 1", "action item 2"]
}}

Transcript:
\"\"\"
{transcript}
\"\"\"
"""


def generate_notes(transcript: str) -> dict:
    """
    Sends the transcript to the local LLM and parses back
    structured notes. Falls back to a safe default if the
    model output isn't valid JSON.
    """
    prompt = PROMPT_TEMPLATE.format(transcript=transcript)

    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
        timeout=120,
    )
    raw_output = response.json().get("response", "")

    try:
        # Grab just the JSON part in case the model adds extra text
        start = raw_output.find("{")
        end = raw_output.rfind("}") + 1
        notes = json.loads(raw_output[start:end])
    except (ValueError, json.JSONDecodeError):
        notes = {
            "summary": raw_output.strip() or "Could not generate summary.",
            "decisions": [],
            "action_items": [],
        }

    return notes
