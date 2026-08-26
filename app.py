from flask import Flask, jsonify, request, Response
import docker
from pymongo import MongoClient
import psutil
import functools
import hmac
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()


def required_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} must be configured")
    return value


USERNAME = required_env('STATUS_SERVER_USERNAME')
PASSWORD = required_env('STATUS_SERVER_PASSWORD')
PORT = int(os.getenv('STATUS_SERVER_PORT', '5000'))

MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_HOST = os.getenv('MONGO_HOST', 'mongodb')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
MONGO_RULES = os.getenv('MONGO_RULES', '?authSource=admin')


def check_auth(username, password):
    return (
        username is not None
        and password is not None
        and hmac.compare_digest(username, USERNAME)
        and hmac.compare_digest(password, PASSWORD)
    )


def authenticate():
    response = Response(
        'Authentication error.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )
    response.headers['Cache-Control'] = 'no-store'
    return response


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
    try:
        client = docker.from_env()
        containers = client.containers.list()
        container_status = {container.name: container.status for container in containers}
        return jsonify(container_status)
    except docker.errors.DockerException as error:
        app.logger.warning("Docker health check failed: %s", type(error).__name__)
        return jsonify({"error": "Docker connection error"}), 503
    finally:
        if 'client' in locals():
            client.close()


@app.route('/status/mongodb')
@requires_auth
def mongodb_status():
    if bool(MONGO_USERNAME) != bool(MONGO_PASSWORD):
        app.logger.warning("MongoDB health check is missing one credential")
        return jsonify({"mongodb": "MongoDB configuration error"}), 503

    credentials = ''
    if MONGO_USERNAME and MONGO_PASSWORD:
        credentials = f"{quote_plus(MONGO_USERNAME)}:{quote_plus(MONGO_PASSWORD)}@"
    mongo_uri = f"mongodb://{credentials}{MONGO_HOST}:{MONGO_PORT}/{MONGO_RULES}"
    try:
        with MongoClient(mongo_uri, serverSelectionTimeoutMS=1000) as mongo_client:
            mongo_client.server_info()
        return jsonify({"mongodb": "running"})
    except Exception as error:
        app.logger.warning("MongoDB health check failed: %s", type(error).__name__)
        return jsonify({"mongodb": "MongoDB connection error"}), 503


@app.route('/status/system')
@requires_auth
def system_status():
    cpu = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory()._asdict()
    disk = psutil.disk_usage('/')._asdict()
    return jsonify({
        "cpu_percent": cpu,
        "memory": memory,
        "disk": disk
    })


@app.route('/healthz')
def healthz():
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
