"""obsidian-mcp - Vault CRUD + Backlinks + Search (Carotis-AI)."""
from __future__ import annotations

import hashlib
import os
import re
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as e:
    raise SystemExit("fastmcp missing. pip install mcp") from e

VAULT_ROOT = Path(
    os.environ.get(
        "CAROTIS_VAULT_ROOT",
        str(Path(__file__).resolve().parents[2]),
    )
).resolve()

ALLOW_WRITE_GLOBS = [
    "memory/runs/**",
    "memory/reflections/**",
    "memory/graph_snapshots/**",
    "memory/anomalies/**",
    "memory/decisions/**",
    "memory/domain/**",
    "outputs/**",
    "data/anonymized/**",
]

DENY_READ_GLOBS = [
    "data/dicom_temp/**",
    "data/raw/**",
    "**/.env",
    "**/secrets/**",
]

SKIP_DIRS = {
    "node_modules", ".git", ".venv", "venv", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".next", "dist", "build",
    ".turbo", "coverage", ".obsidian",
}

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")

mcp = FastMCP("obsidian-mcp")


def _walk_md(root: Path):
    stack = [root]
    while stack:
        cur = stack.pop()
        try:
            for entry in cur.iterdir():
                if entry.is_dir():
                    if entry.name in SKIP_DIRS or entry.name.startswith("."):
                        continue
                    stack.append(entry)
                elif entry.is_file() and entry.suffix.lower() == ".md":
                    yield entry
        except (PermissionError, OSError):
            continue


def _safe_path(rel: str, *, must_exist: bool = False) -> Path:
    p = (VAULT_ROOT / rel).resolve()
    if not str(p).startswith(str(VAULT_ROOT)):
        raise ValueError(f"path-escape: {rel}")
    if must_exist and not p.exists():
        raise FileNotFoundError(rel)
    return p


def _glob_match(rel: str, patterns: list[str]) -> bool:
    rel_norm = rel.replace("\\", "/")
    return any(fnmatch(rel_norm, pat) for pat in patterns)


def _is_writable(rel: str) -> bool:
    return _glob_match(rel, ALLOW_WRITE_GLOBS)


def _is_readable(rel: str) -> bool:
    return not _glob_match(rel, DENY_READ_GLOBS)


def _split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    fm_raw = text[4:end]
    body = text[end + 5:]
    fm: dict = {}
    for line in fm_raw.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm, body


def _extract_wikilinks(text: str) -> list[str]:
    return [m.group(1).strip() for m in WIKILINK_RE.finditer(text)]


@mcp.tool()
def vault_root() -> str:
    """Return the absolute vault-root path."""
    return str(VAULT_ROOT)


@mcp.tool()
def vault_search(query: str, k: int = 10) -> list[dict[str, Any]]:
    """Substring + token-overlap search across .md files in vault."""
    hits: list[tuple[float, str, str]] = []
    q_lower = query.lower()
    q_tokens = set(re.findall(r"\w+", q_lower))
    for md in _walk_md(VAULT_ROOT):
        rel = str(md.relative_to(VAULT_ROOT)).replace("\\", "/")
        if not _is_readable(rel):
            continue
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        text_lower = text.lower()
        score = 0.0
        if q_lower in text_lower:
            score += 5.0 + text_lower.count(q_lower) * 0.5
        if q_tokens:
            tok_overlap = sum(1 for t in q_tokens if t in text_lower)
            score += tok_overlap / max(len(q_tokens), 1)
        if score <= 0:
            continue
        idx = text_lower.find(q_lower) if q_lower in text_lower else 0
        snippet = text[max(0, idx - 80): idx + 240].replace("\n", " ")
        hits.append((score, rel, snippet))
    hits.sort(key=lambda x: -x[0])
    return [{"path": p, "score": round(s, 3), "snippet": sn} for s, p, sn in hits[:k]]


@mcp.tool()
def vault_read(path: str) -> dict[str, Any]:
    rel = path.replace("\\", "/").lstrip("/")
    if not _is_readable(rel):
        raise PermissionError(f"deny-read: {rel}")
    p = _safe_path(rel, must_exist=True)
    text = p.read_text(encoding="utf-8", errors="ignore")
    fm, _ = _split_frontmatter(text)
    return {
        "path": rel,
        "bytes": len(text.encode("utf-8")),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "frontmatter": fm,
        "wikilinks": _extract_wikilinks(text),
        "content": text,
    }


@mcp.tool()
def vault_write(path: str, content: str, append: bool = False) -> dict[str, Any]:
    rel = path.replace("\\", "/").lstrip("/")
    if not _is_writable(rel):
        raise PermissionError(f"deny-write: {rel} not in ALLOW_WRITE_GLOBS")
    p = _safe_path(rel)
    p.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if append else "w"
    with open(p, mode, encoding="utf-8") as f:
        n = f.write(content)
    return {
        "path": rel,
        "bytes_written": n,
        "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
        "mode": mode,
    }


@mcp.tool()
def vault_list(glob: str = "*.md", limit: int = 100) -> list[str]:
    out: list[str] = []
    if glob.endswith(".md") or "*.md" in glob:
        for f in _walk_md(VAULT_ROOT):
            rel = str(f.relative_to(VAULT_ROOT)).replace("\\", "/")
            if not _is_readable(rel):
                continue
            if not fnmatch(rel, glob) and not fnmatch(Path(rel).name, glob):
                continue
            out.append(rel)
            if len(out) >= limit:
                break
    else:
        for f in VAULT_ROOT.rglob(glob):
            rel = str(f.relative_to(VAULT_ROOT)).replace("\\", "/")
            if any(part in SKIP_DIRS for part in Path(rel).parts):
                continue
            if not _is_readable(rel):
                continue
            out.append(rel)
            if len(out) >= limit:
                break
    return out


@mcp.tool()
def vault_backlinks(path: str) -> list[str]:
    rel = path.replace("\\", "/").lstrip("/")
    target = Path(rel).stem
    out: list[str] = []
    for md in _walk_md(VAULT_ROOT):
        r = str(md.relative_to(VAULT_ROOT)).replace("\\", "/")
        if r == rel or not _is_readable(r):
            continue
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for link in _extract_wikilinks(text):
            if link == target or link.endswith("/" + target):
                out.append(r)
                break
    return out


@mcp.tool()
def vault_stats() -> dict[str, Any]:
    n_md = sum(1 for _ in _walk_md(VAULT_ROOT))
    runs_dir = VAULT_ROOT / "memory" / "runs"
    n_runs = sum(1 for _ in runs_dir.glob("*.md")) if runs_dir.exists() else 0
    dec_dir = VAULT_ROOT / "memory" / "decisions"
    n_decisions = sum(1 for _ in dec_dir.glob("*.md")) if dec_dir.exists() else 0
    return {
        "vault_root": str(VAULT_ROOT),
        "n_markdown_files": n_md,
        "n_runs": n_runs,
        "n_decisions": n_decisions,
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
