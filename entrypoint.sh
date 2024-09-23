#!/bin/bash
set -e

# Default DOCKER_GID if not set
DOCKER_GID=${DOCKER_GID:-999}

# Check if docker group exists
if getent group docker > /dev/null; then
  echo "docker-Gruppe existiert bereits mit GID $(getent group docker | grep docker | cut -d: -f3)."
else
  echo "Erstelle docker-Gruppe mit GID $DOCKER_GID."
  groupadd -g $DOCKER_GID docker
fi

# Add user to 'docker' group
usermod -aG docker pythonstatusserveruser

# Execute the CMD
exec gosu pythonstatusserveruser "$@"