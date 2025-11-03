FROM python:3.9-slim

WORKDIR /app

# Use faster apt mirrors and install only essential packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with timeout
RUN pip install --no-cache-dir --timeout 100 -r requirements.txt

# Copy application code
COPY . .

EXPOSE 5000

CMD ["python", "backend/app.py"]