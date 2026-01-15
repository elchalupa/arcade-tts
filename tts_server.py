"""
Arcade TTS Server
A Twitch Channel Point TTS system powered by Chatterbox voice cloning.
https://github.com/elchalupa/arcade-tts
"""

import random
import os
from flask import Flask, request, jsonify
import torchaudio as ta
from chatterbox.tts_turbo import ChatterboxTurboTTS

# ============================================================
# CONFIGURATION
# ============================================================

# Voice reference file (change this to your voice sample)
VOICE_REFERENCE = os.environ.get("VOICE_REFERENCE", "voices/default_voice.wav")

# Output settings
OUTPUT_FOLDER = os.environ.get("OUTPUT_FOLDER", "tts_output")
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "latest_tts.wav")

# Server settings
PORT = int(os.environ.get("PORT", 5000))
HOST = os.environ.get("HOST", "0.0.0.0")

# Available paralinguistic tags
TAGS = ["[sigh]", "[laugh]", "[chuckle]", "[cough]"]

# Tag injection settings
MIN_TAGS = 1
MAX_TAGS = 3

# ============================================================
# INITIALIZATION
# ============================================================

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Initialize Flask app
app = Flask(__name__)

# Load model at startup (this takes a moment)
print("=" * 60)
print("ARCADE TTS SERVER")
print("=" * 60)
print(f"Loading Chatterbox-Turbo model...")
model = ChatterboxTurboTTS.from_pretrained(device="cuda")
print(f"Model loaded!")
print(f"Voice reference: {VOICE_REFERENCE}")
print(f"Output folder: {OUTPUT_FOLDER}")
print("=" * 60)


# ============================================================
# TAG INJECTION
# ============================================================

def inject_tags(text):
    """
    Inject 1-3 random paralinguistic tags at random positions in the text.
    
    Args:
        text: Input text string
        
    Returns:
        Text with tags injected
    """
    words = text.split()
    
    if not words:
        return text
    
    # Decide how many tags (1-3)
    num_tags = random.randint(MIN_TAGS, MAX_TAGS)
    
    # Pick random tags (can repeat)
    tags_to_insert = [random.choice(TAGS) for _ in range(num_tags)]
    
    # Pick random positions (including start and end)
    # Position 0 = before first word, len(words) = after last word
    max_positions = len(words) + 1
    num_positions = min(num_tags, max_positions)
    positions = sorted(
        random.sample(range(max_positions), num_positions),
        reverse=True
    )
    
    # Insert tags at positions (reverse order to preserve indices)
    for i, pos in enumerate(positions):
        if i < len(tags_to_insert):
            words.insert(pos, tags_to_insert[i])
    
    return " ".join(words)


# ============================================================
# API ENDPOINTS
# ============================================================

@app.route("/speak", methods=["GET", "POST"])
def speak():
    """
    Generate TTS from text with random tag injection.
    
    Query params or JSON body:
        text: The text to synthesize
        
    Returns:
        JSON with success status and file path
    """
    # Get text from request
    if request.method == "POST":
        data = request.get_json()
        text = data.get("text", "") if data else ""
    else:
        text = request.args.get("text", "")
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    # Inject random tags
    tagged_text = inject_tags(text)
    print(f"Original: {text}")
    print(f"Tagged: {tagged_text}")
    
    # Generate audio
    try:
        wav = model.generate(tagged_text, audio_prompt_path=VOICE_REFERENCE)
        ta.save(OUTPUT_FILE, wav, model.sr)
        print(f"Saved to {OUTPUT_FILE}")
        
        return jsonify({
            "success": True,
            "original_text": text,
            "tagged_text": tagged_text,
            "output_file": os.path.abspath(OUTPUT_FILE)
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/speak_raw", methods=["GET", "POST"])
def speak_raw():
    """
    Generate TTS from text WITHOUT tag injection.
    
    Query params or JSON body:
        text: The text to synthesize
        
    Returns:
        JSON with success status and file path
    """
    # Get text from request
    if request.method == "POST":
        data = request.get_json()
        text = data.get("text", "") if data else ""
    else:
        text = request.args.get("text", "")
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    print(f"Raw text (no tags): {text}")
    
    # Generate audio
    try:
        wav = model.generate(text, audio_prompt_path=VOICE_REFERENCE)
        ta.save(OUTPUT_FILE, wav, model.sr)
        print(f"Saved to {OUTPUT_FILE}")
        
        return jsonify({
            "success": True,
            "text": text,
            "output_file": os.path.abspath(OUTPUT_FILE)
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "model_loaded": True,
        "voice_reference": VOICE_REFERENCE
    })


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print(f"\nStarting TTS server on http://{HOST}:{PORT}")
    print("")
    print("Endpoints:")
    print(f"  GET/POST http://localhost:{PORT}/speak?text=Your message here")
    print(f"  GET/POST http://localhost:{PORT}/speak_raw?text=Your message here (no tags)")
    print(f"  GET      http://localhost:{PORT}/health")
    print("")
    app.run(host=HOST, port=PORT, threaded=False)
