import os
import json
from pathlib import Path
from uuid import uuid4
from datetime import datetime, timezone

from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
from video_processing.frame_extractor import extract_frames
from video_processing.utils import evidence_to_prompt, frames_to_evidence
from ai.summarizer import generate_summary
from ai.transcriber import transcribe_video

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
OUTPUT_FOLDER = BASE_DIR / "outputs"
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)
app.config["MAX_CONTENT_LENGTH"] = 300 * 1024 * 1024

# Route for serving frames
@app.route('/outputs/<analysis_id>/<filename>')
def get_frame(analysis_id, filename):
    return send_from_directory(OUTPUT_FOLDER / analysis_id, filename)

# Home page
@app.route("/")
def index():
    # The upload screen is now the application's starting point.
    return redirect(url_for("upload"))

# Upload page
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("video")

        if not file or not file.filename:
            return "No file selected"

        filename = secure_filename(file.filename)
        if not filename:
            return "Invalid file name"

        analysis_id = uuid4().hex
        filepath = UPLOAD_FOLDER / f"{analysis_id}_{filename}"
        analysis_folder = OUTPUT_FOLDER / analysis_id
        file.save(filepath)

        try:
            frames = extract_frames(filepath, analysis_folder)
            evidence = frames_to_evidence(frames, analysis_folder)
            transcript = transcribe_video(filepath)
            summary = generate_summary(evidence_to_prompt(evidence), transcript)
            result = {"analysis_id": analysis_id, "created_at": datetime.now(timezone.utc).isoformat(), "source_file": filename, "summary": summary, "transcript": transcript, "key_moments": evidence}
            with (analysis_folder / "analysis.json").open("w", encoding="utf-8") as result_file:
                json.dump(result, result_file, ensure_ascii=False, indent=2)
            return render_template("result.html", summary=summary, evidence=evidence, analysis_id=analysis_id, transcript_available=bool(transcript))
        except Exception as e:
            return f"Error processing video: {str(e)}"

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
