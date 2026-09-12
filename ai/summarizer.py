"""Create complete, evidence-grounded summaries from video transcript and visuals."""

from __future__ import annotations

import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"


def _completion(messages: list[dict], max_tokens: int) -> str:
    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={
            "model": os.getenv("GROQ_SUMMARY_MODEL", "openai/gpt-oss-20b"),
            "temperature": 0.1,
            "max_tokens": max_tokens,
            "messages": messages,
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def _transcript_chunks(transcript: str, limit: int = 6500) -> list[str]:
    """Split at words so long videos do not lose their later content."""
    words = transcript.split()
    chunks, current, length = [], [], 0
    for word in words:
        if current and length + len(word) + 1 > limit:
            chunks.append(" ".join(current))
            current, length = [], 0
        current.append(word)
        length += len(word) + 1
    if current:
        chunks.append(" ".join(current))
    return chunks


def _complete_transcript_evidence(transcript: str) -> str:
    """Preserve all important points from long transcripts before final writing."""
    if len(transcript) <= 18000:
        return transcript

    notes = []
    chunks = _transcript_chunks(transcript)
    for number, chunk in enumerate(chunks, start=1):
        notes.append(_completion([
            {"role": "system", "content": "You extract complete, factual notes from a section of a video transcript."},
            {"role": "user", "content": f"""Create detailed factual notes for transcript section {number} of {len(chunks)}.
Keep every important event, explanation, decision, result, instruction, name, and conclusion.
Do not add anything not said. These notes will be combined into a complete final video summary.

TRANSCRIPT SECTION:
{chunk}"""},
        ], max_tokens=700))
    return "\n\n".join(f"SECTION {index}:\n{note}" for index, note in enumerate(notes, start=1))


def generate_summary(visual_evidence: str, transcript: str = "") -> str:
    if not API_KEY:
        raise RuntimeError("GROQ_API_KEY is not configured.")

    try:
        transcript_evidence = _complete_transcript_evidence(transcript) if transcript else "No transcript available."
        return _completion([
            {"role": "system", "content": "You write accurate, complete, evidence-grounded video summaries."},
            {"role": "user", "content": f"""Write one detailed final summary of this entire video.

Requirements:
- Include all important content supported by the evidence: progression, actions, key explanations, decisions, and conclusions.
- Use the transcript as the primary source for speech; use visual evidence to add visible context and events.
- Do not turn this into a frame-by-frame list. Write 2–4 connected, detailed paragraphs.
- Never invent information. If something cannot be confirmed by the evidence, leave it out.
- Do not mention timestamps, frame names, captions, or the analysis process.

VISUAL EVIDENCE:
{visual_evidence}

FULL TRANSCRIPT EVIDENCE:
{transcript_evidence}
"""},
        ], max_tokens=1000)
    except (requests.RequestException, KeyError, IndexError) as error:
        raise RuntimeError(f"Summary generation failed: {error}") from error
