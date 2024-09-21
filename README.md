
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

- Python 3.7+
- Docker installed and running
- MongoDB instance (local or remote)
- [pip](https://pip.pypa.io/en/stable/) package manager

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/system-status-api.git
   cd system-status-api
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

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
```

Note: Replace the placeholder values with your actual credentials and configuration.

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
```

## Usage

1. **Activate the virtual environment**

   ```bash
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Start the Flask application**

   ```bash
   python app.py
   ```

The API will be available at http://0.0.0.0:5000/, unless you specified a different port in the `.env` file.

## API Endpoints

All endpoints require basic authentication using the USERNAME and PASSWORD defined in the `.env` file.

### 1. Retrieve Docker Container Status

- **Endpoint:** `/status/docker`
- **Method:** `GET`
- **Description:** Retrieves the status of all Docker containers.

**Example Request:**

```bash
curl -u your_username:your_password http://localhost:5000/status/docker
```

**Example Response:**

```json
{
  "container_name_1": "running",
  "container_name_2": "exited",
  ...
}
```

### 2. Retrieve MongoDB Status

- **Endpoint:** `/status/mongodb`
- **Method:** `GET`
- **Description:** Checks the connectivity and status of the MongoDB instance.

**Example Request:**

```bash
curl -u your_username:your_password http://localhost:5000/status/mongodb
```

**Example Response:**

```json
{
  "mongodb": "running"
}
```

**Error Message:**

```json
{
  "mongodb": "MongoDB connection error: mongodb://... || Error message"
}
```

### 3. Retrieve System Status

- **Endpoint:** `/status/system`
- **Method:** `GET`
- **Description:** Retrieves CPU usage, memory usage, and disk usage.

**Example Request:**

```bash
curl -u your_username:your_password http://localhost:5000/status/system
```

**Example Response:**

```json
{
  "cpu_percent": 23.5,
  "memory": {
    "total": 16777216,
    "available": 8388608,
    "percent": 50.0,
    "used": 8388608,
    "free": 8388608
  },
  "disk": {
    "total": 500107862016,
    "used": 250053931008,
    "free": 250053931008,
    "percent": 50.0
  }
}
```

## Environment Variables

| Variable      | Description                                    | Default      |
|---------------|------------------------------------------------|--------------|
| USERNAME      | Username for API authentication                | —            |
| PASSWORD      | Password for API authentication                | —            |
| PORT          | Port on which the Flask app runs               | 5000         |
| MONGO_USERNAME| Username for MongoDB authentication            | —            |
| MONGO_PASSWORD| Password for MongoDB authentication            | —            |
| MONGO_HOST    | Host address for MongoDB                       | —            |
| MONGO_PORT    | Port number for MongoDB                        | 27017        |
| MONGO_RULES   | Additional MongoDB connection parameters       | ?authSource=admin |

## Dependencies

- Flask - Web framework for Python
- docker - Docker SDK for Python
- pymongo - MongoDB driver for Python
- psutil - System and process utilities
- python-dotenv - Load environment variables from a `.env` file

Install all dependencies with:

```bash
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -m "Add a feature"`
4. Push to the branch: `git push origin feature/YourFeature`
5. Open a Pull Request.

Please make sure to update tests as appropriate and ensure the code adheres to the project's coding standards.

## Contact

For questions or suggestions, please open an issue or contact your.email@example.com.
