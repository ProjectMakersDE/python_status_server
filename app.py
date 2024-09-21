from flask import Flask, jsonify, request, Response
import docker
from pymongo import MongoClient
import psutil
import functools
import os
from dotenv import load_dotenv
app = Flask(__name__)
load_dotenv()

# Credentials from environment variables
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
PORT = int(os.getenv('PORT', 5000))

MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
MONGO_RULES = os.getenv('MONGO_RULES', '?authSource=admin')


def check_auth(username, password):
    return username == USERNAME and password == PASSWORD


def authenticate():
    return Response(
        'Authentication error.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_auth(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@app.route('/status/docker')
@requires_auth
def docker_status():
    client = docker.from_env()
    try:
        containers = client.containers.list()
        container_status = {container.name: container.status for container in containers}
        return jsonify(container_status)
    except docker.errors.DockerException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/status/mongodb')
@requires_auth
def mongodb_status():
    mongo_uri = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_RULES}"
    try:
        mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=1000)
        mongo_client.server_info()
        mongo_status = "running"
        return jsonify({"mongodb": mongo_status})
    except Exception as e:
        return jsonify({"mongodb": f"MongoDB connection error: {mongo_uri} || {e}"})


@app.route('/status/system')
@requires_auth
def system_status():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()._asdict()
    disk = psutil.disk_usage('/')._asdict()
    return jsonify({
        "cpu_percent": cpu,
        "memory": memory,
        "disk": disk
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
