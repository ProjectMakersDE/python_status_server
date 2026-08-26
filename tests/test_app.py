import base64
import os
import unittest
from unittest.mock import MagicMock, patch


os.environ.setdefault("STATUS_SERVER_USERNAME", "test-user")
os.environ.setdefault("STATUS_SERVER_PASSWORD", "test-password")
os.environ.setdefault("STATUS_SERVER_PORT", "5000")

import app  # noqa: E402


def auth_header(username="test-user", password="test-password"):
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


class StatusApiTest(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()

    def test_status_endpoints_require_authentication(self):
        response = self.client.get("/status/system")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers["Cache-Control"], "no-store")

    def test_healthz_is_available_without_credentials(self):
        response = self.client.get("/healthz")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "ok"})

    @patch("app.docker.from_env")
    def test_docker_status_closes_client(self, docker_from_env):
        docker_client = MagicMock()
        container = MagicMock()
        container.name = "api"
        container.status = "running"
        docker_client.containers.list.return_value = [container]
        docker_from_env.return_value = docker_client

        response = self.client.get("/status/docker", headers=auth_header())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"api": "running"})
        docker_client.close.assert_called_once()

    @patch("app.MongoClient", side_effect=RuntimeError("database unavailable"))
    def test_mongodb_error_does_not_expose_connection_details(self, _mongo_client):
        with patch.object(app, "MONGO_USERNAME", "mongo-user"), patch.object(
            app, "MONGO_PASSWORD", "very-secret-password"
        ):
            response = self.client.get("/status/mongodb", headers=auth_header())

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json, {"mongodb": "MongoDB connection error"})
        body = response.get_data(as_text=True)
        self.assertNotIn("very-secret-password", body)
        self.assertNotIn("mongodb://", body)


if __name__ == "__main__":
    unittest.main()
