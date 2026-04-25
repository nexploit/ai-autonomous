FROM python:3.11-slim

WORKDIR /app

# Update system packages and install dependencies
RUN apt-get update && apt-get install -y \
    iputils-ping \
    traceroute \
    net-tools \
    nmap \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Upgrade pip and wheel to latest secure versions
RUN pip install --upgrade --no-cache-dir pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
