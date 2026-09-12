"""Extract a small, representative set of frames from one video."""

from __future__ import annotations

from pathlib import Path

import cv2


def _histogram(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    histogram = cv2.calcHist([hsv], [0, 1], None, [16, 16], [0, 180, 0, 256])
    return cv2.normalize(histogram, histogram).flatten()


def _sharpness(frame) -> float:
    return float(cv2.Laplacian(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var())


def extract_frames(video_path: str | Path, output_folder: str | Path, min_frames: int = 6, max_frames: int = 24, candidate_count: int = 120, duplicate_similarity: float = 0.90) -> list[dict]:
    """Save distinct key moments, not routine evenly-spaced screenshots."""
    video_path = Path(video_path)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise ValueError("The uploaded file could not be read as a video.")
    fps = capture.get(cv2.CAP_PROP_FPS) or 0
    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    if fps <= 0 or total_frames <= 0:
        capture.release()
        raise ValueError("The video does not contain readable frame metadata.")

    duration_seconds = total_frames / fps
    # Longer videos receive more visual coverage, while short videos still
    # receive at least six relevant moments when they contain enough variety.
    target_count = min(max_frames, max(min_frames, round(duration_seconds / 12)))
    scan_count = min(max(candidate_count, target_count * 8), total_frames)
    positions = [0] if scan_count == 1 else sorted({round(i * (total_frames - 1) / (scan_count - 1)) for i in range(scan_count)})
    candidates: list[dict] = []
    previous_histogram = None
    for frame_number in positions:
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ok, frame = capture.read()
        if not ok:
            continue
        histogram = _histogram(frame)
        change = 1.0 if previous_histogram is None else 1.0 - cv2.compareHist(previous_histogram, histogram, cv2.HISTCMP_CORREL)
        candidates.append({"frame_number": frame_number, "frame": frame, "histogram": histogram, "score": change + min(_sharpness(frame) / 1000, 0.35)})
        previous_histogram = histogram

    capture.release()
    if not candidates:
        raise ValueError("No readable frames were found in the video.")

    selected: list[dict] = []
    for candidate in sorted(candidates, key=lambda item: item["score"], reverse=True):
        if all(cv2.compareHist(candidate["histogram"], chosen["histogram"], cv2.HISTCMP_CORREL) < duplicate_similarity for chosen in selected):
            selected.append(candidate)
        if len(selected) >= target_count:
            break
    if not selected:
        selected = [candidates[0]]
    selected.sort(key=lambda item: item["frame_number"])

    frames: list[dict] = []
    for position, candidate in enumerate(selected, start=1):
        filename = f"key_moment_{position:02d}.jpg"
        if cv2.imwrite(str(output_folder / filename), candidate["frame"]):
            frames.append({"filename": filename, "timestamp": round(candidate["frame_number"] / fps, 1)})
    return frames
