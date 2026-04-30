"""run_loop.py — Per-Run-Orchestrator für Claude-Sessions.

Pre-Hook (Pflicht am Anfang jedes Runs):
  - Vault-Health (paths, lockfile)
  - Graph-Snapshot rebuild (force False, nur bei Stale)
  - Hermes-Health
  - Ollama-Health
  - Browser-Harness ready (ENV-Check)

Post-Hook (Pflicht am Ende):
  - Letzten Run-Log finden
  - Hermes reflektiert run-log
  - Graph-Snapshot rebuild (force True)
  - MEMORY.md Index-Check
  - Lockfile freigeben

CLI:
  python run_loop.py pre        # vor Session
  python run_loop.py post [run_log_path]  # nach Session
  python run_loop.py status     # Health-Snapshot
  python run_loop.py loop       # pre + post in einem (für Smoke-Tests)
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

try:
    import urllib.request
    _HAS_URL = True
except ImportError:
    _HAS_URL = False

VAULT = Path(
    os.environ.get(
        "CAROTIS_VAULT_ROOT",
        str(Path(__file__).resolve().parents[2]),
    )
).resolve()

# Wir importieren die MCP-Module direkt, ohne stdio. Sie haben Tool-Funktionen
# die wir programmatisch nutzen können.
sys.path.insert(0, str(Path(__file__).parent))


def _import_servers():
    import obsidian_mcp as obs
    import graphify_mcp as gf
    import hermes_mcp as hm
    return obs, gf, hm


def _lock_path() -> Path:
    p = VAULT / "memory" / ".run.lock"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _acquire_lock() -> bool:
    lock = _lock_path()
    if lock.exists():
        try:
            data = json.loads(lock.read_text())
            if time.time() - data.get("ts", 0) < 7200:  # 2h stale
                return False
        except Exception:
            pass
    lock.write_text(json.dumps({"pid": os.getpid(), "ts": time.time()}))
    return True


def _release_lock() -> None:
    lock = _lock_path()
    if lock.exists():
        lock.unlink()


def _docker_compose_file() -> Path:
    # Suche docker-compose.yml relativ zum Vault-Root
    candidates = [
        VAULT / "code" / "docker-compose.yml",
        VAULT / "docker-compose.yml",
        Path(__file__).parent.parent / "docker-compose.yml",
    ]
    for c in candidates:
        if c.exists():
            return c
    return candidates[0]


def _hermes_running() -> bool:
    if not _HAS_URL:
        return False
    try:
        urllib.request.urlopen("http://localhost:8200/health", timeout=3)
        return True
    except Exception:
        return False


def _ollama_running() -> bool:
    if not _HAS_URL:
        return False
    try:
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3)
        return True
    except Exception:
        return False


def _ensure_hermes(max_wait: int = 30) -> dict[str, Any]:
    if _hermes_running():
        return {"action": "already-running"}
    # Versuche Docker
    dc = _docker_compose_file()
    try:
        subprocess.run(
            ["docker", "compose", "-f", str(dc), "up", "-d", "hermes"],
            capture_output=True, text=True, timeout=30, check=False,
        )
    except FileNotFoundError:
        return {"action": "docker-not-found"}
    # Warte auf Health
    for _ in range(max_wait // 2):
        if _hermes_running():
            return {"action": "started", "wait_s": _ * 2}
        time.sleep(2)
    return {"action": "timeout", "wait_s": max_wait}


def _ensure_ollama(max_wait: int = 30) -> dict[str, Any]:
    if _ollama_running():
        return {"action": "already-running"}
    # Versuche ollama serve
    try:
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        return {"action": "ollama-binary-not-found"}
    for _ in range(max_wait // 2):
        if _ollama_running():
            return {"action": "started", "wait_s": _ * 2}
        time.sleep(2)
    return {"action": "timeout", "wait_s": max_wait}


def pre() -> dict[str, Any]:
    obs, gf, hm = _import_servers()
    out: dict[str, Any] = {"phase": "pre", "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
    out["lock_acquired"] = _acquire_lock()
    out["vault"] = {
        "root": str(VAULT),
        "exists": VAULT.exists(),
        "stats": obs.vault_stats(),
    }
    snap = gf.graph_snapshot(force_rebuild=False)
    out["graph"] = snap
    # Auto-Start
    if os.environ.get("CAROTIS_AUTO_START", "1") == "1":
        out["auto_start"] = {
            "hermes": _ensure_hermes(),
            "ollama": _ensure_ollama(),
        }
    out["hermes"] = hm.hermes_health()
    print(json.dumps(out, indent=2, default=str))
    return out


def post(run_log_path: str | None = None) -> dict[str, Any]:
    obs, gf, hm = _import_servers()
    out: dict[str, Any] = {"phase": "post", "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
    # find latest run log
    if not run_log_path:
        runs = sorted(
            (VAULT / "memory" / "runs").glob("*.md"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        run_log_path = (
            str(runs[0].relative_to(VAULT)).replace("\\", "/") if runs else None
        )
    out["run_log"] = run_log_path
    if run_log_path:
        try:
            out["reflection"] = hm.hermes_reflect(run_log_path)
        except Exception as e:
            out["reflection"] = {"error": str(e)}
    out["graph_rebuilt"] = gf.graph_snapshot(force_rebuild=True)
    # MEMORY.md sanity
    mem_index = VAULT / "MEMORY.md"
    if mem_index.exists():
        nlines = sum(1 for _ in mem_index.open(encoding="utf-8"))
        out["memory_md_lines"] = nlines
        if nlines > 200:
            out["warning"] = f"MEMORY.md too long ({nlines} > 200) — consolidate"
    _release_lock()
    out["lock_released"] = True
    print(json.dumps(out, indent=2, default=str))
    return out


def status() -> dict[str, Any]:
    obs, gf, hm = _import_servers()
    snap = gf.graph_snapshot(force_rebuild=False)
    return {
        "vault": obs.vault_stats(),
        "graph": gf.graph_stats(),
        "hermes": hm.hermes_health(),
    }


def loop() -> dict[str, Any]:
    return {"pre": pre(), "post": post()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=["pre", "post", "status", "loop"])
    ap.add_argument("run_log", nargs="?", default=None)
    args = ap.parse_args()
    try:
        if args.phase == "pre":
            pre()
        elif args.phase == "post":
            post(args.run_log)
        elif args.phase == "status":
            print(json.dumps(status(), indent=2, default=str))
        elif args.phase == "loop":
            print(json.dumps(loop(), indent=2, default=str))
    except Exception as e:
        print(json.dumps({"error": str(e), "phase": args.phase}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
