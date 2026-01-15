# 🎮 Arcade TTS

A Twitch Channel Point TTS (Text-to-Speech) system powered by [Chatterbox](https://github.com/resemble-ai/chatterbox) voice cloning. Give your stream a unique voice that reads viewer messages with personality.

## ✨ Features

- **Voice Cloning** — Uses Chatterbox-Turbo for high-quality voice synthesis
- **Paralinguistic Tags** — Randomly injects `[sigh]`, `[laugh]`, `[chuckle]`, `[cough]` for personality
- **Streamer.bot Integration** — HTTP API for easy automation
- **Channel Point Redemptions** — Viewers redeem points, their message gets read aloud
- **Multiple Voice Profiles** — Support for different voices (e.g., dry sardonic bot, yelling jumpscare)
- **Cloud-Ready** — Dockerized for deployment to RunPod Serverless or similar

## 🎬 Demo

*Coming soon — link to Twitch clip*

## 📋 Requirements

- Python 3.11
- NVIDIA GPU with CUDA support (for local use)
- ~4GB VRAM minimum (RTX 3060 or better recommended)
- [Streamer.bot](https://streamer.bot/) v1.0.3+

## 🚀 Quick Start (Local)

### 1. Clone the Repository

```bash
git clone https://github.com/elchalupa/arcade-tts.git
cd arcade-tts
```

### 2. Create Virtual Environment

```bash
py -3.11 -m venv venv
.\venv\Scripts\Activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install PyTorch with CUDA

```bash
pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124
```

### 5. Login to Hugging Face

Chatterbox-Turbo requires authentication:

```bash
huggingface-cli login
```

### 6. Add Your Voice Reference

Place a ~10 second WAV file in the `voices/` folder. Update the `VOICE_REFERENCE` path in `tts_server.py` if needed.

### 7. Start the Server

```bash
python tts_server.py
```

Or use the batch file:

```bash
start_tts.bat
```

### 8. Test It

```bash
curl "http://localhost:5000/speak?text=Hello%20world"
```

Audio will be saved to `tts_output/latest_tts.wav`.

## 🤖 Streamer.bot Setup

### Create an Action

1. Create a new Action called "TTS Redeem"
2. Add the following sub-actions:

**Sub-action 1: Fetch URL**
- URL: `http://localhost:5000/speak?text=%rawInput%`
- Variable: `ttsResponse`

**Sub-action 2: Delay**
- Milliseconds: `8000` (adjust based on generation speed)

**Sub-action 3: Play Sound**
- File: `C:\path\to\arcade-tts\tts_output\latest_tts.wav`
- Audio Device: Your stream output

### Link to Channel Point Reward

1. Create a Channel Point Reward in Twitch/Streamer.bot
2. Enable "Require Viewer to Enter Text"
3. Add trigger: Channel Point Reward Redemption → Your TTS Reward

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/speak?text=...` | GET/POST | Generate TTS with random tag injection |
| `/speak_raw?text=...` | GET/POST | Generate TTS without tags |
| `/health` | GET | Health check |

### Response Format

```json
{
  "success": true,
  "original_text": "Hello world",
  "tagged_text": "[sigh] Hello world",
  "output_file": "C:/path/to/tts_output/latest_tts.wav"
}
```

## 🎭 Paralinguistic Tags

The server randomly injects 1-3 tags per message at random positions:

- `[sigh]` — Exasperated exhale
- `[laugh]` — Laughter
- `[chuckle]` — Soft laugh
- `[cough]` — Clearing throat

Use `/speak_raw` to disable tag injection.

## 🐳 Docker Deployment

### Build Locally

```bash
docker build -t arcade-tts .
```

### Run Locally

```bash
docker-compose up
```

### Deploy to RunPod Serverless

See [DEPLOYMENT.md](DEPLOYMENT.md) for cloud deployment instructions.

## 📁 Project Structure

```
arcade-tts/
├── tts_server.py           # Main Flask server
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container definition
├── docker-compose.yml      # Local Docker setup
├── start_tts.bat           # Windows startup script
├── stop_tts.bat            # Windows shutdown script
├── .env.example            # Environment template
├── voices/                 # Voice reference files
│   └── README.md
└── tts_output/             # Generated audio (gitignored)
```

## ⚙️ Configuration

Edit `tts_server.py` to customize:

```python
VOICE_REFERENCE = "voices/your_voice.wav"  # Voice clone source
OUTPUT_FOLDER = "tts_output"                # Output directory
PORT = 5000                                  # Server port
TAGS = ["[sigh]", "[laugh]", "[chuckle]", "[cough]"]  # Available tags
```

## 🔧 Troubleshooting

### "CUDA not available"
- Ensure NVIDIA drivers are installed
- Reinstall PyTorch with CUDA: `pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124`

### "Model loading failed"
- Run `huggingface-cli login` and enter your token
- Ensure you have internet access for first-time model download

### "Audio sounds wrong"
- Voice reference should be ~10 seconds of clear audio
- Minimize background noise in reference clip
- Try a different reference sample

### High GPU memory usage
- Chatterbox-Turbo uses ~4GB VRAM
- Close other GPU-intensive applications
- Consider cloud deployment for streaming

## 🙏 Credits

- [Chatterbox](https://github.com/resemble-ai/chatterbox) by Resemble AI — The TTS engine
- [Streamer.bot](https://streamer.bot/) — Stream automation
- [CREMA-D Dataset](https://github.com/CheyneyComputerScience/CREMA-D) — Emotional voice samples

## 📄 License

MIT License — See [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

---

Made with ❤️ for the streaming community
