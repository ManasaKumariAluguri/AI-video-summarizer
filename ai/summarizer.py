import requests
import os
API_KEY = os.getenv("GROQ_API_KEY")
def generate_summary(text):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
    "model": "llama-3.1-8b-instant",
    "messages": [
        {"role": "user", "content": f"""
You are an AI video analyzer.

Based on the following sequence of frames:
{text}

Create a realistic and meaningful summary of what is happening in the video.
Do not mention frame names. Describe it like a story of what you understood.
"""}
    ]
}

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    # 🔥 PRINT ACTUAL RESPONSE
    print("API RESPONSE:", result)

    # ✅ SAFE CHECK
    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        return f"ERROR: {result}"