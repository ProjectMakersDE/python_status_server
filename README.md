
# System Status API

A Flask-based API for monitoring Docker containers, MongoDB status, and system resources. This application provides secure endpoints to retrieve real-time information about your system's Docker containers, MongoDB instance, and overall system performance.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Dependencies](#dependencies)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

## Features

- **Docker Status:** Retrieve the status of all Docker containers.
- **MongoDB Status:** Check the connectivity and status of a MongoDB instance.
- **System Status:** Retrieve real-time information on CPU, memory, and disk usage.
- **Basic Authentication:** Secure the endpoints with a username and password.

## Prerequisites

- Docker installed and running
- MongoDB instance (local or remote)

## Installation

### Using Docker Compose

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/system-status-api.git
   cd system-status-api
   ```

2. **Create a `.env` file** (Refer to the Configuration section below for required variables)

3. **Run Docker Compose**

   ```bash
   docker-compose up -d
   ```

The API will be available at `http://0.0.0.0:5000/` unless you specified a different port in the `.env` file.

## Configuration

### Environment Variables

Create a `.env` file in the project's root directory and define the following variables:

```env
# Flask App Configuration
USERNAME=your_username
PASSWORD=your_password
PORT=5000

# MongoDB Configuration
MONGO_USERNAME=your_mongo_username
MONGO_PASSWORD=your_mongo_password
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_RULES=?authSource=admin

# Docker Configuration
DOCKER_GID=999  # Replace with your actual Docker group GID
DOCKER_NETWORK=network_name  # Optional: Specify the Docker network to use
```

To get your Docker GID, execute the following command on your host:

```bash
getent group docker | cut -d: -f3
```

This ensures that the Docker container can access the Docker socket on the host.

### Example .env file

```env
USERNAME=admin
PASSWORD=secret
PORT=5000

MONGO_USERNAME=mongoUser
MONGO_PASSWORD=mongoPass
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_RULES=?authSource=admin

DOCKER_GID=999
DOCKER_NETWORK=dockerNetwork
```

## Docker Compose Configuration

The `docker-compose.yml` file should look like this:

```yaml
services:
  pythonstatusserver:
    build:
      context: .
      args:
        DOCKER_GID: ${DOCKER_GID}
    image: projectmakers/pythonstatusserver:latest
    container_name: pythonstatusserver
    ports:
      - "${PORT}:${PORT}"
    environment:
      - USERNAME=${USERNAME}
      - PASSWORD=${PASSWORD}
      - PORT=${PORT}
      - MONGO_USERNAME=${MONGO_USERNAME}
      - MONGO_PASSWORD=${MONGO_PASSWORD}
      - MONGO_HOST=${MONGO_HOST}
      - MONGO_PORT=${MONGO_PORT}
      - MONGO_RULES=${MONGO_RULES}
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    restart: unless-stopped
    networks:
      - ${DOCKER_NETWORK}

networks:
  pm_network:
    external: true
    name: ${DOCKER_NETWORK}
```

## API Endpoints

Refer to the existing documentation for the API endpoints and their usage.

## Dependencies

- Docker - Required for running the API and accessing system status information
- MongoDB - Required for MongoDB status monitoring

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please follow the steps mentioned above.

## Contact

For questions or suggestions, please open an issue or contact your.email@example.com.
