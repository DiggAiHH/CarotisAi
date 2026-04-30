#!/usr/bin/env python3
"""Hermes + Ollama + Browser Harness Healthcheck

Produces a JSON or Markdown report of the local AI stack status.
No patient data is accessed or transmitted by this script.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

import requests

DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_HERMES_URL = "http://localhost:8200"


@dataclass
class CheckResult:
    name: str
    status: str  # "ok", "warn", "error"
    message: str
    details: dict = field(default_factory=dict)


def check_ollama(ollama_url: str) -> CheckResult:
    try:
        resp = requests.get(f"{ollama_url}/api/tags", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        models = [m.get("name", m.get("model", "?")) for m in data.get("models", [])]
        return CheckResult(
            name="Ollama",
            status="ok",
            message=f"Running - {len(models)} model(s) available",
            details={"models": models, "url": ollama_url},
        )
    except requests.exceptions.ConnectionError as exc:
        return CheckResult(
            name="Ollama",
            status="error",
            message=f"Connection refused - {exc}",
            details={"url": ollama_url},
        )
    except requests.exceptions.RequestException as exc:
        return CheckResult(
            name="Ollama",
            status="error",
            message=f"Request failed - {exc}",
            details={"url": ollama_url},
        )


def check_hermes(hermes_url: str) -> CheckResult:
    try:
        resp = requests.get(f"{hermes_url}/health", timeout=10)
        resp.raise_for_status()
        data = (
            resp.json()
            if resp.headers.get("content-type", "").startswith("application/json")
            else {}
        )
        return CheckResult(
            name="Hermes",
            status="ok",
            message="Healthy",
            details={"url": hermes_url, "response": data},
        )
    except requests.exceptions.ConnectionError as exc:
        return CheckResult(
            name="Hermes",
            status="error",
            message=f"Connection refused — {exc}",
            details={"url": hermes_url},
        )
    except requests.exceptions.RequestException as exc:
        return CheckResult(
            name="Hermes",
            status="error",
            message=f"Request failed — {exc}",
            details={"url": hermes_url},
        )


def check_skills(hermes_url: str) -> CheckResult:
    try:
        resp = requests.get(f"{hermes_url}/v1/skills", timeout=10)
        if resp.status_code == 404:
            # Fallback: try legacy endpoint or inspect local skills dir
            skills_dir = Path(__file__).resolve().parent.parent / "hermes" / "skills"
            if skills_dir.exists():
                skills = [p.name for p in skills_dir.iterdir() if p.suffix == ".md"]
                return CheckResult(
                    name="Skills",
                    status="warn",
                    message=f"Hermes skills endpoint not exposed - found {len(skills)} local skill file(s)",
                    details={"local_skills": skills},
                )
            return CheckResult(
                name="Skills",
                status="warn",
                message="Skills endpoint not available and no local skill dir found",
                details={},
            )
        resp.raise_for_status()
        data = resp.json()
        skills = data.get("skills", [])
        return CheckResult(
            name="Skills",
            status="ok",
            message=f"{len(skills)} skill(s) loaded",
            details={"skills": skills},
        )
    except requests.exceptions.RequestException as exc:
        skills_dir = Path(__file__).resolve().parent.parent / "hermes" / "skills"
        if skills_dir.exists():
            skills = [p.name for p in skills_dir.iterdir() if p.suffix == ".md"]
            return CheckResult(
                name="Skills",
                status="warn",
                message=f"Request failed - {exc}; found {len(skills)} local skill file(s)",
                details={"local_skills": skills},
            )
        return CheckResult(
            name="Skills",
            status="warn",
            message=f"Request failed — {exc}",
            details={},
        )


def check_browser_harness(hermes_url: str) -> CheckResult:
    try:
        # Attempt to read Hermes config via a metadata endpoint or fall back to local file
        config_path = Path(__file__).resolve().parent.parent / "hermes" / "config.toml"
        if config_path.exists():
            import toml

            cfg = toml.load(config_path)
            browser_cfg = cfg.get("browser", {})
            enabled = browser_cfg.get("enabled", False)
            allowed = browser_cfg.get("allowed_hosts", [])
            if enabled:
                return CheckResult(
                    name="Browser Harness",
                    status="ok",
                    message=f"Enabled - {len(allowed)} allowed host(s)",
                    details={
                        "allowed_hosts": allowed,
                        "mcp_server": browser_cfg.get("mcp_server", "?"),
                    },
                )
            return CheckResult(
                name="Browser Harness",
                status="warn",
                message="Disabled in config",
                details={"config_path": str(config_path)},
            )

        # Try remote endpoint if available
        resp = requests.get(f"{hermes_url}/v1/config", timeout=10)
        if resp.status_code == 404:
            return CheckResult(
                name="Browser Harness",
                status="warn",
                message="Config endpoint not available and local config not found",
                details={},
            )
        resp.raise_for_status()
        cfg = resp.json()
        browser_cfg = cfg.get("browser", {})
        enabled = browser_cfg.get("enabled", False)
        return CheckResult(
            name="Browser Harness",
            status="ok" if enabled else "warn",
            message="Enabled" if enabled else "Disabled",
            details=browser_cfg,
        )
    except Exception as exc:
        return CheckResult(
            name="Browser Harness",
            status="warn",
            message=f"Could not verify - {exc}",
            details={},
        )


def render_markdown(results: list[CheckResult]) -> str:
    lines = ["# Hermes Health Report\n"]
    for r in results:
        icon = {"ok": "[OK]", "warn": "[WARN]", "error": "[ERR]"}.get(r.status, "[?]")
        lines.append(f"## {icon} {r.name} — {r.status.upper()}")
        lines.append(f"{r.message}\n")
        if r.details:
            lines.append("```json")
            lines.append(json.dumps(r.details, indent=2, ensure_ascii=False))
            lines.append("```\n")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Hermes stack healthcheck")
    parser.add_argument(
        "--ollama-url", default=DEFAULT_OLLAMA_URL, help="Ollama base URL"
    )
    parser.add_argument(
        "--hermes-url", default=DEFAULT_HERMES_URL, help="Hermes base URL"
    )
    parser.add_argument(
        "--format", choices=["json", "md"], default="md", help="Output format"
    )
    args = parser.parse_args()

    results: list[CheckResult] = []
    results.append(check_ollama(args.ollama_url))
    results.append(check_hermes(args.hermes_url))
    results.append(check_skills(args.hermes_url))
    results.append(check_browser_harness(args.hermes_url))

    if args.format == "json":
        print(json.dumps([asdict(r) for r in results], indent=2, ensure_ascii=False))
    else:
        print(render_markdown(results))

    # Exit non-zero if any check is in error state
    if any(r.status == "error" for r in results):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
