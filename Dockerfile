FROM python:3.11-slim

WORKDIR /app

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

# Copy backend sources and install
COPY backend/requirements.txt ./
RUN pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt
COPY backend/ .

ENV PORT=8000
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
