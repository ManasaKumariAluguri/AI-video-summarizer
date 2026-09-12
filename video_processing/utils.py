"""Turn timestamped video frames into grounded visual evidence."""

from __future__ import annotations

from pathlib import Path

from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor

_processor = None
_model = None


def _captioning_model():
    global _processor, _model
    if _processor is None or _model is None:
        _processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        _model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        _model.eval()
    return _processor, _model


def format_timestamp(seconds: float) -> str:
    minutes, remaining = divmod(int(seconds), 60)
    return f"{minutes}:{remaining:02d}"


def frames_to_evidence(frames: list[dict], folder_path: str | Path) -> list[dict]:
    processor, model = _captioning_model()
    folder_path = Path(folder_path)
    evidence: list[dict] = []
    for frame in frames:
        with Image.open(folder_path / frame["filename"]) as image:
            inputs = processor(images=image.convert("RGB"), return_tensors="pt")
        output = model.generate(**inputs, max_new_tokens=40)
        caption = processor.decode(output[0], skip_special_tokens=True).strip()
        if caption:
            evidence.append({**frame, "time_label": format_timestamp(frame["timestamp"]), "caption": caption})
    if not evidence:
        raise ValueError("The selected frames could not be captioned.")
    return evidence


def evidence_to_prompt(evidence: list[dict]) -> str:
    return "\n".join(f"[{item['time_label']}] {item['caption']}" for item in evidence)
