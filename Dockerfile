# Use a more compatible CUDA base image
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

WORKDIR /app

# Set non-interactive frontend to avoid timezone prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    git \
    tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY check_gpu.py .
EXPOSE 5000

# Create a wrapper file to initialize our class and expose the app
# We can specify an initial model via environment variable
RUN echo 'import os; from app import WhisperAPI; initial_model = os.environ.get("WHISPER_MODEL", "base"); whisper_api = WhisperAPI(initial_model); app = whisper_api.app' > wsgi.py

# Force PyTorch to use CUDA
ENV CUDA_VISIBLE_DEVICES=0
ENV NVIDIA_VISIBLE_DEVICES=all

# Increased timeout to handle longer audio processing
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app", "--workers=1", "--timeout", "300"]
