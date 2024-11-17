FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN \
    apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose the port for FastAPI
EXPOSE 8000

# Run FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]