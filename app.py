import os
from flask import Flask, render_template, request, send_from_directory
from video_processing.frame_extractor import extract_frames
from video_processing.utils import frames_to_text
from ai.summarizer import generate_summary

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Route for serving frames
@app.route('/outputs/frames/<filename>')
def get_frame(filename):
    return send_from_directory('outputs/frames', filename)

# Home page
@app.route("/")
def index():
    return render_template("index.html")

# Upload page
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["video"]

        if file.filename == "":
            return "No file selected"

        # Optional: Add file type validation here
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        try:
            # Step 1: Extract frames
            extract_frames(filepath)

            # Step 2: Convert frames → text
            text = frames_to_text()

            # Step 3: Generate summary
            summary = generate_summary(text)

            return render_template("result.html", summary=summary)
        except Exception as e:
            return f"Error processing video: {str(e)}"

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))