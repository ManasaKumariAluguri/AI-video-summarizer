# 🎥 AI Video Understanding & Summarization Platform

An AI-powered Flask web application that analyzes uploaded videos and generates detailed, evidence-grounded summaries using both **visual content** and **spoken audio**.

The application extracts representative key moments from a video, generates captions for those frames using the **Salesforce BLIP image-captioning model**, optionally transcribes the video's audio using **Groq Whisper**, and combines the visual and transcript evidence to generate a final summary using a Groq-hosted Large Language Model.

---

## ✨ Features

- 📤 Upload videos through a web interface
- 🎞️ Extract representative key moments using OpenCV
- 🧠 Select visually meaningful frames instead of simple screenshots
- 🖼️ Generate image captions using Salesforce BLIP
- 🎙️ Transcribe spoken content using Groq Whisper
- 🤖 Generate AI-powered video summaries using Groq LLM
- 📝 Combine visual and transcript evidence for better summaries
- 🔍 Preserve important events and explanations from long videos
- 📊 Display extracted key moments alongside the generated summary
- ⏳ Clean web interface with loading feedback
- 💾 Save analysis results as JSON
- 📁 Organize outputs by unique analysis ID

---

## 🧠 How It Works

The application follows this pipeline:

```text
                ┌─────────────────┐
                │   Upload Video  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Extract Frames  │
                │    OpenCV       │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Select Key      │
                │    Moments      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ BLIP Image      │
                │ Captioning      │
                └────────┬────────┘
                         │
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ▼                                 ▼
┌─────────────────┐              ┌─────────────────┐
│ Video Audio     │              │ Visual Evidence │
│ Transcription   │              │    Captions     │
│ Groq Whisper    │              │      BLIP       │
└────────┬────────┘              └────────┬────────┘
         │                                │
         └───────────────┬────────────────┘
                         ▼
                ┌─────────────────┐
                │   Groq LLM      │
                │ Summary Engine  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Final Video     │
                │    Summary      │
                └─────────────────┘
```


🛠️ Tech Stack
Backend
- Python
- Flask
Video Processing
- OpenCV
- Pillow
AI / Machine Learning
- Hugging Face Transformers
- Salesforce BLIP
- PyTorch
- Groq API
- Whisper transcription
Frontend
- HTML
- CSS
- JavaScript
Configuration
- python-dotenv
- Environment variables

📂 Project Structure
AI-video-summarizer/
│
├── ai/
│   ├── summarizer.py
│   ├── transcriber.py
│   └── caption_generator.py
│
├── video_processing/
│   ├── frame_extractor.py
│   └── utils.py
│
├── templates/
│   ├── upload.html
│   └── result.html
│
├── static/
│   └── ...
│
├── uploads/
│   └── ...
│
├── outputs/
│   └── ...
│
├── app.py
├── config.py
├── requirements.txt
├── runtime.txt
├── Procfile
├── .gitignore
└── README.md

⚙️ Requirements
Before running the project, make sure you have:
- Python 3.x
- pip
- Git
- A Groq API key
- Internet connection for downloading the BLIP model

🚀 Installation
1. Clone the repository
git clone https://github.com/ManasaKumariAluguri/AI-video-summarizer.git
2. Navigate into the project
cd AI-video-summarizer
3. Create a virtual environment
Windows
python -m venv venv
Activate it:
venv\Scripts\activate
macOS / Linux
python3 -m venv venv
Activate it:
source venv/bin/activate
📦 Install Dependencies
pip install -r requirements.txt
The project uses:
flask
opencv-python
requests
transformers
torch
pillow
python-dotenv
🔐 Environment Variables
Create a .env file in the project root:
GROQ_API_KEY=your_groq_api_key_here
Optional model configuration
The summarization model can be configured using:
GROQ_SUMMARY_MODEL=openai/gpt-oss-20b
The transcription model can be configured using:
GROQ_TRANSCRIPTION_MODEL=whisper-large-v3-turbo
Example:
GROQ_API_KEY=your_groq_api_key_here
GROQ_SUMMARY_MODEL=openai/gpt-oss-20b
GROQ_TRANSCRIPTION_MODEL=whisper-large-v3-turbo
⚠️ Never commit your real API key to GitHub.

▶️ Run the Application
Activate your virtual environment first.
Then run:
python app.py
The Flask server will start on:
http://127.0.0.1:5000
Open the URL in your browser.

🎬 Using the Application
Step 1 — Upload a Video
Open the application in your browser and upload a video.
Step 2 — Frame Extraction
The application analyzes the video and selects representative key moments.
Instead of simply taking screenshots at fixed intervals, the frame extractor considers visual changes and frame sharpness to select meaningful frames.
Step 3 — Visual Understanding
The selected frames are processed using:
Salesforce/blip-image-captioning-base
BLIP generates captions describing the visual content of each selected frame.
Step 4 — Audio Transcription
If a valid Groq API key is available, the application's transcription component attempts to extract spoken content using:
whisper-large-v3-turbo
Step 5 — AI Summarization
The visual evidence and transcript are provided to the Groq LLM.
The default summarization model is:
openai/gpt-oss-20b
The model generates a detailed summary based only on the available evidence.
Step 6 — Results
The application displays:
- AI-generated summary
- Extracted key moments
- Visual captions
- Transcript availability
- Analysis results
The analysis data is also stored as an analysis.json file inside the corresponding output directory.
📊 Video Processing
The frame extraction system is designed to select representative key moments rather than generating a large number of redundant frames.
The number of selected frames depends on video duration, with configurable minimum and maximum limits.
The system also compares visual similarity between frames to reduce duplicate content.
🧠 AI Summarization
The summarizer combines two sources of evidence:
Visual Evidence
Generated from selected video frames using BLIP:
Video Frame
     ↓
BLIP Image Captioning
     ↓
Visual Description
Transcript Evidence
Generated from the video's audio:
Video Audio
     ↓
Groq Whisper
     ↓
Transcript
Both are then provided to the LLM:
Visual Evidence + Transcript
             ↓
          Groq LLM
             ↓
       Final Summary
For longer transcripts, the application divides the transcript into sections and creates intermediate factual notes before producing the final summary.
📁 Output Structure
Each video analysis receives a unique analysis ID.
The output structure is similar to:
outputs/
└── <analysis_id>/
    ├── key_moment_01.jpg
    ├── key_moment_02.jpg
    ├── key_moment_03.jpg
    ├── ...
    └── analysis.json
The analysis.json file contains information such as:
- Analysis ID
- Creation time
- Original filename
- Generated summary
- Transcript
- Key visual moments
🔒 Security
Do not commit secrets to GitHub.
Your .env file should remain local:
GROQ_API_KEY=your_secret_key
Make sure .env is included in .gitignore.
If an API key is accidentally exposed publicly, revoke it and generate a new one.
📌 Current API Configuration
The application communicates with Groq using an OpenAI-compatible chat completion endpoint.
The summarization model can be controlled through:
GROQ_SUMMARY_MODEL
The default model configured by the application is:
openai/gpt-oss-20b
The transcription model can be controlled through:
GROQ_TRANSCRIPTION_MODEL
The default transcription model is:
whisper-large-v3-turbo
🧪 Example Workflow
Upload video
     ↓
Extract representative frames
     ↓
Generate BLIP captions
     ↓
Transcribe audio
     ↓
Combine visual + transcript evidence
     ↓
Send evidence to Groq LLM
     ↓
Generate detailed summary
     ↓
Display summary + key moments

🔮 Future Enhancements
Possible improvements include:
- 🎯 More advanced scene detection
- 🌍 Multi-language transcription
- 🗣️ Speaker identification
- 📑 Export summaries as PDF
- 🔎 Search inside video transcripts
- ⏱️ Clickable timestamps
- 📊 Video analytics dashboard
- ☁️ Cloud deployment
- 👤 User authentication
- 🗄️ Persistent database storage
- 🎞️ Support for additional video formats

👩‍💻 Author
Manasa Kumari Aluguri
GitHub:
https://github.com/ManasaKumariAluguri
