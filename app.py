from flask import Flask, request, jsonify, abort
from tempfile import NamedTemporaryFile
import whisper, torch
import os

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("tiny", device=DEVICE)  # Changed from "base" to "tiny"

app = Flask(__name__)

@app.route("/")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/whisper", methods=["POST"])
def transcribe():
    if "file" not in request.files:
        abort(400, description="Missing 'file' form field.")

    f = request.files["file"]
    with NamedTemporaryFile(suffix=os.path.splitext(f.filename)[1], delete=False) as tmp:
        f.save(tmp.name)
    try:
        res = model.transcribe(tmp.name)
        return jsonify({"filename": f.filename, "text": res["text"]})
    finally:
        os.remove(tmp.name)
