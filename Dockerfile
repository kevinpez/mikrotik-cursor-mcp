FROM python:3.10-slim

# Install required system dependencies
RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up work directory
WORKDIR /app

# Install MCP package and other dependencies
RUN pip install --no-cache-dir mcp>=0.1.0
RUN pip install --no-cache-dir logger

# Copy the requirements file if exists
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project structure
COPY . .

# Set the entrypoint to run the server
ENTRYPOINT ["python", "/app/src/main.py"]