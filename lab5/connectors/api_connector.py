"""HTTP API connector for Lab 5."""

import json
import urllib.error
import urllib.request
from urllib.parse import urlsplit


class APIConnector:
    name = "api_connector"

    description = "Calls the local Lab 2 course-management API."

    BASE_URL = "http://127.0.0.1:8000"

    ALLOWED_PATHS = {
        "/",
        "/health",
        "/courses",
        "/courses/count",
        "/courses/summary",
    }

    def get(self, path):
        """Make a GET request to an allowed local API endpoint."""

        if not isinstance(path, str):
            raise ValueError("API path must be text.")

        if (
            not path.startswith("/")
            or path.startswith("//")
            or "://" in path
        ):
            raise ValueError("Provide a valid API path.")

        parsed = urlsplit(path)

        if parsed.scheme or parsed.netloc:
            raise ValueError("Only API paths are allowed.")

        if parsed.query or parsed.fragment:
            raise ValueError(
                "Query strings and fragments are not supported."
            )

        if parsed.path not in self.ALLOWED_PATHS:
            raise ValueError("This API endpoint is not allowed.")

        request = urllib.request.Request(
            self.BASE_URL + path,
            headers={"Accept": "application/json"},
            method="GET",
        )

        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                body = response.read(100_000).decode("utf-8")

                try:
                    data = json.loads(body)
                except json.JSONDecodeError:
                    data = body

                return {
                    "status_code": response.status,
                    "data": data,
                }

        except urllib.error.HTTPError as error:
            return {
                "status_code": error.code,
                "error": "The API returned an HTTP error.",
            }

        except urllib.error.URLError as error:
            raise ConnectionError(
                "Could not connect to the Lab 2 API. "
                "Start the Lab 2 API server first."
            ) from error