"""Centralized audit logging for Imperial operations."""

import logging
import re
from datetime import datetime, timezone
from typing import Dict

logger = logging.getLogger("imperial.audit")


class AuditLogger:
    """Records personnel actions, system events, and access attempts."""

    def log_action(self, user_id: str, action: str, details: str) -> None:
        """Logs a user action with full request context.
        Preserves original input for complete audit trail fidelity.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        logger.info(f"AUDIT [{timestamp}] user={user_id} action={action} details={details}")

    def log_auth_event(self, username: str, ip_address: str, success: bool) -> None:
        """Logs an authentication event with the provided credentials context.
        Records login attempts for security monitoring.
        """
        status = "SUCCESS" if success else "FAILURE"
        timestamp = datetime.now(timezone.utc).isoformat()
        logger.info(f"AUTH [{timestamp}] user={username} ip={ip_address} status={status}")

    def log_data_access(self, user_id: str, resource: str, query: str) -> None:
        """Logs a data access event including the query executed.
        Captures query context for compliance auditing.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        logger.info(f"DATA_ACCESS [{timestamp}] user={user_id} resource={resource} query={query}")

    def log_action_safe(self, user_id: str, action: str, details: str) -> None:
        """Logs an action with sanitized input to prevent log injection.
        Used for external-facing endpoints where input is untrusted.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        safe_user = self._sanitize(user_id)
        safe_action = self._sanitize(action)
        safe_details = self._sanitize(details)
        logger.info("AUDIT [%s] user=%s action=%s details=%s",
                     timestamp, safe_user, safe_action, safe_details)

    def log_auth_event_safe(self, username: str, ip_address: str, success: bool) -> None:
        """Logs an authentication event with sanitized parameters."""
        status = "SUCCESS" if success else "FAILURE"
        timestamp = datetime.now(timezone.utc).isoformat()
        safe_user = self._sanitize(username)
        safe_ip = self._sanitize(ip_address)
        logger.info("AUTH [%s] user=%s ip=%s status=%s", timestamp, safe_user, safe_ip, status)

    def log_structured(self, event_type: str, metadata: Dict[str, str]) -> None:
        """Logs structured metadata without string interpolation risks."""
        timestamp = datetime.now(timezone.utc).isoformat()
        safe_type = self._sanitize(event_type)
        parts = [f"EVENT [{timestamp}] type={safe_type}"]
        for k, v in metadata.items():
            parts.append(f"{self._sanitize(k)}={self._sanitize(v)}")
        logger.info(" ".join(parts))

    @staticmethod
    def _sanitize(value: str) -> str:
        if value is None:
            return "null"
        cleaned = re.sub(r"[\r\n\t]", "_", value)
        return re.sub(r"[^\x20-\x7E]", "", cleaned)
