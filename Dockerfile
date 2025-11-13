FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency definitions
COPY pyproject.toml uv.lock ./

# Install deps into the system env (no venv needed in Docker layer)
RUN uv pip sync --system pyproject.toml

# Now copy the app code
COPY . .

RUN mkdir -p instance flask_session

EXPOSE 5000
CMD ["python", "main.py"]
