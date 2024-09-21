# Basis-Image
FROM python:3.11

# Arbeitsverzeichnis festlegen
WORKDIR /app

# Systemabhängigkeiten installieren
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    useradd -m pythonstatusserveruser

# Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Anwendungscode kopieren
COPY app.py .

RUN mkdir -p /app && \
    chown -R pythonstatusserveruser:pythonstatusserveruser /app && \
    chmod -R 755 /app \

USER pythonstatusserveruser

# Umgebungsvariablen für Flask setzen
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Port freigeben
EXPOSE 5000

# Docker-Socket mounten (für Zugriff auf Docker-Daemon)
VOLUME /var/run/docker.sock:/var/run/docker.sock

# Startbefehl
CMD ["python", "app.py"]
