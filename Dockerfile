# Arcade TTS Dockerfile
# For deployment to RunPod Serverless or similar GPU cloud providers

FROM pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install PyTorch with CUDA (already in base image, but ensure correct version)
RUN pip install --no-cache-dir torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124

# Copy application code
COPY tts_server.py .
COPY voices/ ./voices/

# Create output directory
RUN mkdir -p tts_output

# Set environment variables
ENV PORT=5000
ENV HOST=0.0.0.0
ENV VOICE_REFERENCE=voices/default_voice.wav
ENV OUTPUT_FOLDER=tts_output

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the server
CMD ["python", "tts_server.py"]
