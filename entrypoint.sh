#!/bin/sh
set -eu

# The Docker socket is typically group-owned. Resolve its actual GID at
# runtime instead of relying on an image-specific or hard-coded GID, then drop
# privileges before the web server starts.
if [ "$(id -u)" -eq 0 ] && [ -S /var/run/docker.sock ]; then
    docker_gid="$(stat -c '%g' /var/run/docker.sock)"
    docker_group="$(getent group "${docker_gid}" | cut -d: -f1 || true)"

    if [ -z "${docker_group}" ]; then
        docker_group="docker-socket"
        groupadd -g "${docker_gid}" "${docker_group}"
    fi

    usermod -aG "${docker_group}" app
fi

if [ "$(id -u)" -eq 0 ]; then
    exec su -s /bin/sh app -c 'exec "$@"' app "$@"
fi

exec "$@"
