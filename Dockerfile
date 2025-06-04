# Use official Python runtime as base image
FROM python:3.9-slim

# Set maintainer label
LABEL maintainer="your.email@projetct.com"
LABEL version="1.0.0"
LABEL description="Wyscout Data Glossary Scraper"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config.py .
COPY setup.py .

# Create necessary directories
RUN mkdir -p /app/output /app/data/images /app/logs

# Create non-root user for security
RUN groupadd -r scraper && useradd -r -g scraper scraper
RUN chown -R scraper:scraper /app
USER scraper

# Expose port (if needed for future web interface)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import src.scraper; print('OK')" || exit 1

# Default command
CMD ["python", "-m", "src.scraper"]