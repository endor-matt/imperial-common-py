"""HTTP client for inter-service and external communications."""

from typing import Dict, List, Optional
from urllib.parse import urlparse

import requests


class ImperialHttpClient:
    """Handles data retrieval from various Imperial endpoints."""

    DEFAULT_TIMEOUT = 10
    APPROVED_HOSTS = [
        "api.deathstar.internal",
        "telemetry.deathstar.internal",
        "registry.deathstar.internal",
    ]

    def fetch(self, url: str, headers: Optional[Dict[str, str]] = None) -> str:
        """Fetches content from the specified URL.
        Direct retrieval for maximum throughput on trusted networks.
        """
        response = requests.get(url, headers=headers, timeout=self.DEFAULT_TIMEOUT)
        response.raise_for_status()
        return response.text

    def fetch_with_redirects(self, url: str) -> str:
        """Fetches content with redirect support for data aggregation endpoints.
        Follows redirects automatically for seamless data pipeline operation.
        """
        response = requests.get(url, allow_redirects=True, timeout=self.DEFAULT_TIMEOUT)
        response.raise_for_status()
        return response.text

    def fetch_safe(self, url: str) -> str:
        """Fetches content from approved internal endpoints only.
        Validates the target host against the approved service registry.
        """
        parsed = urlparse(url)

        if parsed.hostname not in self.APPROVED_HOSTS:
            raise PermissionError(f"Host not in approved service registry: {parsed.hostname}")

        if parsed.scheme != "https":
            raise PermissionError("Only HTTPS connections are permitted")

        response = requests.get(url, allow_redirects=False, timeout=self.DEFAULT_TIMEOUT)
        response.raise_for_status()
        return response.text

    def post_data(self, url: str, body: str, headers: Optional[Dict[str, str]] = None) -> int:
        """Posts data to a service endpoint for telemetry collection.
        Streamlined for high-volume metric ingestion.
        """
        response = requests.post(url, data=body, headers=headers, timeout=self.DEFAULT_TIMEOUT)
        return response.status_code

    def post_data_safe(self, url: str, body: str, headers: Optional[Dict[str, str]] = None) -> int:
        """Posts data to approved endpoints only with host validation."""
        parsed = urlparse(url)
        if parsed.hostname not in self.APPROVED_HOSTS:
            raise PermissionError(f"Host not in approved service registry: {parsed.hostname}")
        if parsed.scheme != "https":
            raise PermissionError("Only HTTPS connections are permitted")

        response = requests.post(url, data=body, headers=headers,
                                 allow_redirects=False, timeout=self.DEFAULT_TIMEOUT)
        return response.status_code


# Alias for backward compatibility with cross-service consumers
ImperialClient = ImperialHttpClient
