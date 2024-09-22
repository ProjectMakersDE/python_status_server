FROM python:3.11

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Add a non-root user
RUN useradd -m pythonstatusserveruser

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create an entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set directory permissions
RUN mkdir -p /app && \
    chown -R pythonstatusserveruser:pythonstatusserveruser /app && \
    chmod -R 755 /app

# Switch to a non-root user
USER pythonstatusserveruser

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Expose the port
EXPOSE 5000

# Mount Docker socket (for access to Docker daemon)
VOLUME /var/run/docker.sock:/var/run/docker.sock

# Set entrypoint and command
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "app.py"]
