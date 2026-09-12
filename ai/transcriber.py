"""Optional Groq transcription used to ground summaries in spoken content."""

from __future__ import annotations

import os
from pathlib import Path

import requests


def transcribe_video(video_path: str | Path) -> str:
    """Return a transcript when Groq accepts the file; otherwise use visuals only."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return ""
    try:
        with Path(video_path).open("rb") as media:
            response = requests.post(
                "https://api.groq.com/openai/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {api_key}"},
                data={"model": os.getenv("GROQ_TRANSCRIPTION_MODEL", "whisper-large-v3-turbo")},
                files={"file": (Path(video_path).name, media, "application/octet-stream")},
                timeout=120,
            )
        if response.ok:
            return response.json().get("text", "").strip()
    except requests.RequestException:
        pass
    return ""
