# Stage 1: build dependencies
FROM python:3.10-slim AS build

WORKDIR /app

RUN apt-get update \
 && apt-get install -y git ffmpeg build-essential \
 && pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: final runtime
FROM python:3.10-slim

WORKDIR /app

# Copy Python deps from build stage
COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# Install runtime tools
RUN apt-get update && apt-get install -y ffmpeg curl && apt-get clean

COPY app.py .
EXPOSE 5000

# Increased timeout to handle longer audio processing
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers=2", "--timeout", "300"]
