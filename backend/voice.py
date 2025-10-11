from flask import Flask, request, send_file
from flask_cors import CORS
import requests
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://192.168.56.1:8080", "https://xxxxx.ngrok.io"]}})



@app.route("/api/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text", "")
    if not text:
        return {"error": "Metin boş olamaz"}, 400

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    payload = {
        "text": text,
        "voice_settings": {"stability": 0.4, "similarity_boost": 0.9}
    }

    r = requests.post(url, json=payload, headers=headers)
    if r.status_code != 200:
        return {"error": r.text}, r.status_code

    return send_file(BytesIO(r.content), mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
