FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

# Install System Dependencies (Python + common tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv using the official image (reliable method)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
# ENV PATH is not needed for uv as it is in /usr/local/bin

WORKDIR /app

# Copy requirements first to leverage cache
COPY requirements.txt .

# Install dependencies
# Using system python for simplicity in this container
RUN uv pip install --system --index-strategy unsafe-best-match --extra-index-url https://download.pytorch.org/whl/cu121 -r requirements.txt

# Copy application code
COPY . .

# Expose the port
EXPOSE 8100

# Run the application
CMD ["python3", "main.py"]
