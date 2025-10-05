
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p flask_session instance

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Run database migrations on startup (if needed)
# RUN python -c "from app import create_app; from db_init import db; app = create_app(); app.app_context().push(); db.create_all()"

# Expose port
EXPOSE 8080

# Run the application
CMD exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120 --access-logfile - --error-logfile -
