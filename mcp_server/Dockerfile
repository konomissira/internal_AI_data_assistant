FROM python:3.11-slim

WORKDIR /app

# System deps (psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app code
COPY mcp_server /app/mcp_server

EXPOSE 8000

CMD ["uvicorn", "mcp_server.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
