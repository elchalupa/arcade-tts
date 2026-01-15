# Contributing to Arcade TTS

Thanks for your interest in contributing! Here's how you can help.

## Ways to Contribute

### 🐛 Bug Reports
- Open an issue with steps to reproduce
- Include your OS, Python version, GPU model
- Attach relevant logs

### 💡 Feature Requests
- Open an issue describing the feature
- Explain the use case / why it's useful
- Bonus: Suggest an implementation approach

### 🔧 Code Contributions
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test locally
5. Submit a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/arcade-tts.git
cd arcade-tts

# Create virtual environment
py -3.11 -m venv venv
.\venv\Scripts\Activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124

# Login to Hugging Face
huggingface-cli login

# Run the server
python tts_server.py
```

## Code Style

- Follow PEP 8
- Add docstrings to functions
- Comment complex logic
- Keep functions focused and small

## Testing

Before submitting a PR:
1. Test the `/speak` endpoint
2. Test the `/speak_raw` endpoint
3. Test the `/health` endpoint
4. Verify tag injection works as expected

## Questions?

Open an issue or reach out on the stream!
