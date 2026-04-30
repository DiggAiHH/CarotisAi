"""CLI tool to generate a time-limited demo token for Prof. Rohde.

Usage:
    python scripts/generate_rohde_token.py --label "Rohde Demo"
    python scripts/generate_rohde_token.py --expires-days 14 --max-requests 100
    python scripts/generate_rohde_token.py --dry-run

The raw token is printed ONCE and must be sent to the recipient via a
secure channel (e.g. encrypted mail or in-person handoff).  The hashed
token is stored in the local SQLite database.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import secrets
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Allow imports from backend/ when script is run from repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.core.config import get_settings
from app.db.database import init_db, get_session_factory
from app.db.models import DemoToken


def _generate_token() -> str:
    """Generate a URL-safe random token (32+ chars, 256-bit entropy)."""
    return secrets.token_urlsafe(32)


def _hash_token(token: str) -> str:
    """SHA-256 hash of the raw token (same algorithm as security.py)."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


async def _token_exists(token_hash: str) -> bool:
    """Check whether a token hash already exists in the DB."""
    factory = get_session_factory()
    async with factory() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(DemoToken).where(DemoToken.token_hash == token_hash)
        )
        return result.scalar_one_or_none() is not None


async def _insert_token(
    token_hash: str,
    label: str,
    expires_at: datetime,
    max_requests: int,
    rohde_tag: bool,
) -> None:
    """Insert the hashed token into the SQLite demo_tokens table."""
    factory = get_session_factory()
    async with factory() as session:
        token = DemoToken(
            token_hash=token_hash,
            label=label,
            expires_at=expires_at,
            requests_used=0,
            max_requests=max_requests,
            rohde_tag=rohde_tag,
        )
        session.add(token)
        await session.commit()


async def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a secure demo token for Carotis-AI."
    )
    parser.add_argument(
        "--label",
        default="Demo Token",
        help="Human-readable label for the token (default: 'Demo Token')",
    )
    parser.add_argument(
        "--expires-days",
        type=int,
        default=14,
        help="Token validity in days (default: 14)",
    )
    parser.add_argument(
        "--max-requests",
        type=int,
        default=100,
        help="Maximum API requests allowed (default: 100)",
    )
    parser.add_argument(
        "--rohde-tag",
        action="store_true",
        default=True,
        help="Mark token as Rohde-specific (default: True)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print token without writing to database",
    )
    args = parser.parse_args()

    # Generate token
    raw_token = _generate_token()
    token_hash = _hash_token(raw_token)

    # Ensure uniqueness (collision is astronomically unlikely, but defensive)
    while await _token_exists(token_hash):
        raw_token = _generate_token()
        token_hash = _hash_token(raw_token)

    expires_at = datetime.now(timezone.utc) + timedelta(days=args.expires_days)

    print("=" * 60)
    print("Carotis-AI Demo Token Generator")
    print("=" * 60)
    print(f"\nLabel:           {args.label}")
    print(f"Expires:         {expires_at.isoformat()} ({args.expires_days} days)")
    print(f"Max requests:    {args.max_requests}")
    print(f"Rohde tag:       {args.rohde_tag}")
    print(f"\nRAW TOKEN (send this to the recipient):\n{raw_token}\n")

    if args.dry_run:
        print("[DRY-RUN] Token NOT saved to database.")
        print("=" * 60)
        return 0

    # Ensure DB exists
    await init_db()

    await _insert_token(
        token_hash=token_hash,
        label=args.label,
        expires_at=expires_at,
        max_requests=args.max_requests,
        rohde_tag=args.rohde_tag,
    )

    print("Token hash saved to database.")
    print("=" * 60)
    print("\nSECURITY REMINDER:")
    print("- Send the RAW token via encrypted channel only.")
    print("- The token is single-use-display: it will not be shown again.")
    print("- Store it in your password manager until handoff.")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
