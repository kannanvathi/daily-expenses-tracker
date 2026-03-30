FROM python:3.11

# Use /app as the container workspace and copy only the backend sources
WORKDIR /app

# Copy backend directory from the repo root into the image. This makes the
# Dockerfile resilient whether Render builds with context "." or "backend".
COPY backend/ /app/

# Install build dependencies required by some Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libssl-dev \
    libffi-dev \
    cargo \
    python3-dev \
    && rm -rf /var/lib/apt/lists/* || true

# Install Python dependencies from the copied requirements.txt
RUN pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r /app/requirements.txt

ENV PORT=8000
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
