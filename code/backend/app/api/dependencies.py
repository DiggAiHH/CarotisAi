"""Re-export auth functions from security.py for route dependencies.

Kept as a separate module so routes can depend on app.api.dependencies
without pulling in the full security module if they only need basic auth.
"""
from __future__ import annotations

from app.core.security import verify_admin_key, verify_api_key

__all__ = ["verify_admin_key", "verify_api_key"]
