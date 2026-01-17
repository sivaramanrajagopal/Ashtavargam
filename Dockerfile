# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for pyswisseph
# pyswisseph requires SQLite, math libraries, and other system libraries
RUN apt-get update && apt-get install -y \
    libsqlite3-dev \
    sqlite3 \
    build-essential \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Railway will set PORT env variable)
EXPOSE 5004

# Run the application
# Railway sets PORT env variable, app_complete.py reads it
CMD ["python", "app_complete.py"]

