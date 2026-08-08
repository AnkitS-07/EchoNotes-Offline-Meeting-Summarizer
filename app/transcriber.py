"""
Transcriber module - wraps faster-whisper.
Runs 100% locally on CPU or GPU. No internet needed after the model
is downloaded once.
"""

from faster_whisper import WhisperModel

# "base" is a good balance of speed vs accuracy for a demo.
# Options: tiny, base, small, medium, large-v3
MODEL_SIZE = "base"

# compute_type="int8" keeps it fast and light on CPU-only machines.
model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")


def transcribe(audio_path: str) -> str:
    """
    Transcribes an audio file and returns the full text.
    """
    segments, _info = model.transcribe(audio_path, beam_size=5)

    full_text = " ".join(segment.text.strip() for segment in segments)
    return full_text.strip()
