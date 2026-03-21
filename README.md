# AI Video Understanding & Summarization Platform

## Overview
This project is an AI-powered web application that analyzes videos and generates meaningful summaries.

It extracts frames from a video, uses an image captioning model to understand visual content, and generates a summary using a Large Language Model (LLM).

## Features
- 📤 Upload video
- 🎞 Extract frames using OpenCV
- 🧾 Generate captions using BLIP model
- 🤖 AI-generated video summary
- 🎨 Clean and modern UI with pastel design
- ⏳ Loading spinner for better UX

## Tech Stack
- Python
- Flask
- OpenCV
- Transformers (BLIP model)
- Groq API (LLM)
- HTML, CSS

## How It Works
1. User uploads video  
2. Frames are extracted  
3. Each frame is converted into captions  
4. Captions are sent to LLM  
5. AI generates summary  
6. Results displayed with frames  

## Project Structure
video-ai-project/
│── app.py
│── ai/
│── video_processing/
│── templates/
│── static/
│── uploads/
│── outputs/
│── requirements.txt