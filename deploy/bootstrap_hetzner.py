#!/usr/bin/env python3
"""Bootstrap Hetzner host via SSH password auth.

Security:
    Do not hardcode credentials. Provide the root password via the
    HETZNER_ROOT_PASSWORD environment variable for the current shell only.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import paramiko


HOST = os.environ.get("HETZNER_HOST", "204.168.230.127")
PORT = int(os.environ.get("HETZNER_PORT", "22"))
USER = os.environ.get("HETZNER_USER", "root")
PASSWORD = os.environ.get("HETZNER_ROOT_PASSWORD")
DEPLOY_KEY_PATH = Path("deploy/hetzner_deploy_key.pub")


def _deploy_key() -> str:
    if not DEPLOY_KEY_PATH.exists():
        raise FileNotFoundError(f"Missing public key: {DEPLOY_KEY_PATH}")
    key = DEPLOY_KEY_PATH.read_text(encoding="utf-8").strip()
    if not key.startswith(("ssh-ed25519 ", "ssh-rsa ")):
        raise ValueError("Deploy public key format looks invalid")
    return key


def _steps(public_key: str) -> list[tuple[str, str]]:
    return [
        ("mkdir -p /root/.ssh && chmod 700 /root/.ssh", "Create .ssh dir"),
        (
            f"grep -qxF '{public_key}' /root/.ssh/authorized_keys || echo '{public_key}' >> /root/.ssh/authorized_keys",
            "Add deploy SSH key idempotently",
        ),
        ("chmod 600 /root/.ssh/authorized_keys && echo KEY_OK", "Lock authorized_keys"),
        (
            "apt-get update -qq && apt-get install -y docker.io docker-compose-plugin ca-certificates curl rsync && echo DOCKER_INSTALL_OK",
            "Install Docker and deploy dependencies",
        ),
        ("systemctl enable docker && systemctl start docker && echo DOCKER_STARTED", "Start Docker"),
        ("docker --version && docker compose version", "Verify Docker"),
        ("mkdir -p /opt/carotis-ai && echo DIR_OK", "Create app dir"),
        ("echo BOOTSTRAP_COMPLETE", "Done"),
    ]


def run_steps(client: paramiko.SSHClient, public_key: str) -> None:
    for command, description in _steps(public_key):
        print(f"\n--- {description} ---")
        stdin, stdout, stderr = client.exec_command(command, timeout=180)
        out = stdout.read().decode("utf-8", errors="replace")
        err = stderr.read().decode("utf-8", errors="replace")
        if out.strip():
            print("OUT:", out.strip())
        if err.strip():
            print("ERR:", err.strip())
        exit_code = stdout.channel.recv_exit_status()
        if exit_code != 0:
            print(f"[WARN] Exit code {exit_code} for: {description}")
        else:
            print(f"[OK] {description}")
        time.sleep(0.5)


def main() -> int:
    if not PASSWORD:
        print("HETZNER_ROOT_PASSWORD is not set.", file=sys.stderr)
        return 2

    public_key = _deploy_key()
    print(f"Connecting to {HOST}:{PORT} as {USER} ...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            HOST,
            port=PORT,
            username=USER,
            password=PASSWORD,
            allow_agent=False,
            look_for_keys=False,
            timeout=15,
        )
        print("Connected.")
        run_steps(client, public_key)
        return 0
    except Exception as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1
    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(main())
