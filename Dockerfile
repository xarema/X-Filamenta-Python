FROM python:3.12-slim
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "60", "backend.wsgi:app"]
# Run Gunicorn

    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/').read()" || exit 1
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
# Health check

EXPOSE 8000
# Expose port

USER appuser
    chown -R appuser:appuser /app
RUN useradd -m -u 1000 appuser && \
# Create non-root user for security

RUN pip install -e .
# Install application

COPY . .
# Copy application

    pip install gunicorn
    pip install -r requirements.txt && \
RUN pip install --upgrade pip setuptools wheel && \
# Install Python dependencies

COPY requirements.txt .
# Copy requirements

    && rm -rf /var/lib/apt/lists/*
    gcc \
RUN apt-get update && apt-get install -y --no-install-recommends \
# Install system dependencies

WORKDIR /app
# Set work directory

    PIP_DISABLE_PIP_VERSION_CHECK=1
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
ENV PYTHONUNBUFFERED=1 \
# Set environment variables


