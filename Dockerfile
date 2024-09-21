# Base image
FROM python:3.11

# Build argument for Docker group ID with a default value
ARG DOCKER_GID=999

# Set working directory
WORKDIR /app

# Install system dependencies and create Docker group
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -g ${DOCKER_GID} docker \
    && useradd -m -G docker pythonstatusserveruser

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Set directory permissions
RUN mkdir -p /app && \
    chown -R pythonstatusserveruser:pythonstatusserveruser /app && \
    chmod -R 755 /app

# Switch to the new user
USER pythonstatusserveruser

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Expose the port
EXPOSE 5000

# Mount Docker socket (for access to Docker daemon)
VOLUME /var/run/docker.sock:/var/run/docker.sock

# Start command
CMD ["python", "app.py"]
