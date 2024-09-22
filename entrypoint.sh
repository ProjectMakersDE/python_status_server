#!/bin/bash
set -e

# Default DOCKER_GID if not set
DOCKER_GID=${DOCKER_GID:-999}

# Check if group 'docker' exists
if ! getent group docker > /dev/null; then
  echo "docker group dose not exist: GID: $DOCKER_GID."
  exec "$@"
fi

# Add user to 'docker' group
usermod -aG docker pythonstatusserveruser

exec "$@"