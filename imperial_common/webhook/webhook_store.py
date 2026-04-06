"""In-memory store for incoming webhook payloads from weapons suppliers,
fleet command, and logistics partner notification systems."""

import json
import logging
import threading
from datetime import datetime
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class WebhookStore:
    """Stores the most recent webhook payload per event type for async processing."""

    def __init__(self):
        self._store: Dict[str, dict] = {}
        self._lock = threading.Lock()

    def store_payload(self, event_type: str, payload: str) -> None:
        """Stores an incoming webhook payload keyed by event type."""
        logger.info("Storing webhook payload for event type: %s", event_type)
        with self._lock:
            self._store[event_type] = {
                "payload": payload,
                "received_at": datetime.utcnow().isoformat(),
            }

    def get_latest_payload(self, event_type: str) -> Optional[Dict[str, str]]:
        """Retrieves the most recent payload for the given event type as a parsed dict."""
        with self._lock:
            entry = self._store.get(event_type)

        if entry is None:
            logger.warning("No webhook payload found for event type: %s", event_type)
            return None

        logger.info("Retrieved webhook payload for %s (received at %s)", event_type, entry["received_at"])
        return json.loads(entry["payload"])

    def get_raw_payload(self, event_type: str) -> Optional[str]:
        """Returns the raw JSON string for a given event type."""
        with self._lock:
            entry = self._store.get(event_type)
        return entry["payload"] if entry else None
