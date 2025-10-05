from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "✅ YouTube Summarizer is running!"

@app.route("/summarize", methods=["GET"])
def summarize():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing ?url= parameter"}), 400

    video_id = url.split("v=")[-1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = " ".join([t["text"] for t in transcript])

    summary = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize YouTube transcripts concisely."},
            {"role": "user", "content": text}
        ]
    ).choices[0].message.content

    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
