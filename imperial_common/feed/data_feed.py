"""Client for fetching real-time data feeds from external weapons suppliers
and intelligence partner APIs."""

import logging
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class DataFeedClient:
    """Fetches operational data from external supplier and intelligence feeds."""

    DEFAULT_TIMEOUT = 10

    def __init__(self, base_url: str = "https://suppliers.deathstar.internal"):
        self.base_url = base_url

    def fetch_supplier_inventory(self, supplier_id: str) -> List[Dict[str, str]]:
        """Fetches the latest supplier inventory data from the external feed API.

        Returns a list of inventory records, each containing item name,
        category, and pricing values from the external source.
        """
        url = f"{self.base_url}/api/suppliers/{supplier_id}/inventory"
        logger.info("Fetching supplier inventory from feed: %s", url)

        try:
            response = requests.get(url, timeout=self.DEFAULT_TIMEOUT)
            response.raise_for_status()
            records = response.json()
            logger.info("Received %d inventory records for supplier %s", len(records), supplier_id)
            return records
        except Exception as e:
            logger.error("Failed to fetch supplier inventory for %s: %s", supplier_id, e)
            return []

    def fetch_crew_roster(self, unit_id: str) -> List[Dict[str, str]]:
        """Fetches crew roster updates from the external personnel feed.

        Returns structured records from the partner API response.
        """
        url = f"{self.base_url}/api/units/{unit_id}/roster"
        logger.info("Fetching crew roster from feed: %s", url)

        try:
            response = requests.get(url, timeout=self.DEFAULT_TIMEOUT)
            response.raise_for_status()
            records = response.json()
            logger.info("Received %d roster records for unit %s", len(records), unit_id)
            return records
        except Exception as e:
            logger.error("Failed to fetch crew roster for %s: %s", unit_id, e)
            return []
