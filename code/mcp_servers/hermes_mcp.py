"""hermes-mcp - Proxy zu Hermes-Agent (Carotis-AI Self-Improving Layer)."""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

try:
    import urllib.error
    import urllib.request
    from mcp.server.fastmcp import FastMCP
except ImportError as e:
    raise SystemExit("fastmcp missing. pip install mcp") from e

VAULT_ROOT = Path(
    os.environ.get(
        "CAROTIS_VAULT_ROOT",
        str(Path(__file__).resolve().parents[2]),
    )
).resolve()
HERMES = os.environ.get("HERMES_ENDPOINT", "http://localhost:8200")
OLLAMA = os.environ.get("OLLAMA_ENDPOINT", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("HERMES_DEFAULT_MODEL", "mistral:7b")
COMPRESS_MODEL = os.environ.get("HERMES_COMPRESS_MODEL", "qwen3:4b")

REFLECTIONS_DIR = VAULT_ROOT / "memory" / "reflections"
try:
    REFLECTIONS_DIR.mkdir(parents=True, exist_ok=True)
except (PermissionError, OSError):
    pass

mcp = FastMCP("hermes-mcp")


def _http(method: str, url: str, payload: dict | None = None, timeout: int = 60) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8")
        try:
            return json.loads(body)
        except Exception:
            return {"raw": body, "status": resp.status}


def _ollama_chat(prompt: str, model: str, system: str | None = None, timeout: int = 600) -> dict:
    payload: dict[str, Any] = {"model": model, "prompt": prompt, "stream": False}
    if system:
        payload["system"] = system
    return _http("POST", f"{OLLAMA}/api/generate", payload, timeout)


def _try_hermes(method: str, path: str, payload: dict | None = None, timeout: int = 60):
    try:
        r = _http(method, f"{HERMES}{path}", payload, timeout)
        return True, r
    except (urllib.error.URLError, ConnectionError, TimeoutError, OSError) as e:
        return False, {"error": str(e), "fallback": "ollama-direct"}


@mcp.tool()
def hermes_health() -> dict[str, Any]:
    """Check Hermes API + Ollama. Returns aggregated status."""
    out: dict[str, Any] = {"hermes_endpoint": HERMES, "ollama_endpoint": OLLAMA}
    ok_h, r_h = _try_hermes("GET", "/health", timeout=5)
    out["hermes"] = r_h if ok_h else {"reachable": False, "err": r_h.get("error")}
    out["hermes_reachable"] = ok_h
    try:
        r_o = _http("GET", f"{OLLAMA}/api/tags", timeout=5)
        out["ollama"] = {
            "reachable": True,
            "models": [m.get("name") for m in r_o.get("models", [])],
        }
    except Exception as e:
        out["ollama"] = {"reachable": False, "err": str(e)}
    return out


@mcp.tool()
def hermes_list_skills() -> list[str]:
    """List available Hermes skills (from filesystem skill-dir)."""
    skill_dir = VAULT_ROOT / "code" / "hermes" / "skills"
    if not skill_dir.exists():
        return []
    return sorted(p.stem for p in skill_dir.glob("*.md"))


@mcp.tool()
def hermes_call_skill(skill: str, args: dict | None = None, timeout_s: int = 300) -> dict[str, Any]:
    """Invoke a Hermes skill by name. Falls back to ollama-direct if API down."""
    args = args or {}
    ok, r = _try_hermes("POST", f"/skills/{skill}/run", {"args": args}, timeout=timeout_s)
    if ok:
        return r
    skill_file = VAULT_ROOT / "code" / "hermes" / "skills" / f"{skill}.md"
    if not skill_file.exists():
        return {"error": "hermes-down + skill-not-found", "skill": skill}
    spec = skill_file.read_text(encoding="utf-8")
    prompt = (
        f"Du bist der Hermes-Agent. Skill-Spec:\n{spec}\n\n"
        f"Args (JSON): {json.dumps(args, ensure_ascii=False)}\n\n"
        "Fuehre den Skill aus und antworte als JSON."
    )
    r2 = _ollama_chat(prompt, DEFAULT_MODEL, timeout=timeout_s)
    return {
        "skill": skill,
        "fallback": "ollama-direct",
        "response": r2.get("response", ""),
        "model": DEFAULT_MODEL,
    }


@mcp.tool()
def hermes_reflect(run_log_path: str) -> dict[str, Any]:
    """Self-improving layer: analyse a run-log, write reflection."""
    rel = run_log_path.replace("\\", "/").lstrip("/")
    p = (VAULT_ROOT / rel).resolve()
    if not str(p).startswith(str(VAULT_ROOT)) or not p.exists():
        return {"error": "run_log not found", "path": rel}
    text = p.read_text(encoding="utf-8", errors="ignore")
    prompt = (
        "Du bist Hermes, der Self-Improving-Layer von Carotis-AI. "
        "Analysiere folgenden Run-Log und liefere strukturiertes JSON mit "
        "{novelty_score, key_insights, stale_memories, suggested_new_memories, next_actions}.\n\n"
        f"Run-Log:\n{text}"
    )
    ok, r = _try_hermes(
        "POST", "/skills/decision-pattern-miner/run",
        {"args": {"run_log": text}}, timeout=300,
    )
    if ok:
        reflection = r.get("output", json.dumps(r))
    else:
        rr = _ollama_chat(prompt, DEFAULT_MODEL, timeout=300)
        reflection = rr.get("response", "")
    ts = time.strftime("%Y-%m-%dT%H-%M-%S")
    out_name = f"reflection_{Path(rel).stem}_{ts}.md"
    out_path = REFLECTIONS_DIR / out_name
    try:
        out_path.write_text(
            f"---\nsource: {rel}\ntimestamp: {ts}\nmodel: hermes\n---\n\n{reflection}\n",
            encoding="utf-8",
        )
    except (PermissionError, OSError) as e:
        return {"error": f"write-failed: {e}", "source": rel}
    return {
        "reflection_path": str(out_path.relative_to(VAULT_ROOT)).replace("\\", "/"),
        "source": rel,
        "bytes": out_path.stat().st_size,
    }


@mcp.tool()
def hermes_compress(file_path: str, target_tokens: int = 1500) -> dict[str, Any]:
    """Compress a memory/doc file with caveman-compress style."""
    rel = file_path.replace("\\", "/").lstrip("/")
    p = (VAULT_ROOT / rel).resolve()
    if not str(p).startswith(str(VAULT_ROOT)) or not p.exists():
        return {"error": "file not found"}
    text = p.read_text(encoding="utf-8", errors="ignore")
    prompt = (
        f"Komprimiere folgenden Markdown-Text auf ca. {target_tokens} Tokens "
        "im caveman-compress Stil: keine Floskeln, technische Fakten, "
        "[thing][action][reason] Pattern. Code-Bloecke und Pfade unveraenderlich.\n\n"
        f"Original:\n{text}"
    )
    r = _ollama_chat(prompt, COMPRESS_MODEL, timeout=300)
    out = p.with_name(p.stem + "_compressed.md")
    try:
        out.write_text(
            f"---\nsource: {rel}\ntarget_tokens: {target_tokens}\nmodel: {COMPRESS_MODEL}\n---\n\n"
            + r.get("response", ""),
            encoding="utf-8",
        )
    except (PermissionError, OSError) as e:
        return {"error": f"write-failed: {e}"}
    ratio = len(out.read_text()) / max(len(text), 1)
    return {
        "compressed_path": str(out.relative_to(VAULT_ROOT)).replace("\\", "/"),
        "ratio": round(ratio, 3),
        "model": COMPRESS_MODEL,
    }


@mcp.tool()
def hermes_function_call(name: str, args: dict | None = None) -> dict[str, Any]:
    """Generic function-calling endpoint (alias of skill-call)."""
    return hermes_call_skill(name, args or {})


@mcp.tool()
def hermes_chat(prompt: str, model: str | None = None, system: str | None = None) -> dict[str, Any]:
    """Direct chat through Ollama (bypassing skill-routing)."""
    m = model or DEFAULT_MODEL
    r = _ollama_chat(prompt, m, system=system)
    return {"model": m, "response": r.get("response", ""), "done": r.get("done", True)}


if __name__ == "__main__":
    mcp.run(transport="stdio")
