FROM python:3.12-slim

# Install common dev tools agents might invoke
RUN apt-get update && apt-get install -y \
    git curl nodejs npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Workspace is where agents write code
RUN mkdir -p /app/workspace

CMD ["python", "orchestrate.py"]