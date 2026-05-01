"""graphify-mcp - Knowledge-Graph aus Vault-Wikilinks (Carotis-AI)."""
from __future__ import annotations

import json
import os
import re
import time
from collections import defaultdict, deque
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

SNAPSHOT_DIR = VAULT_ROOT / "memory" / "graph_snapshots"
try:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
except (PermissionError, OSError):
    pass
LATEST = SNAPSHOT_DIR / "latest.json"

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md)(?:#[^)]*)?\)")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TAGS_RE = re.compile(r"^tags:\s*(.+)$", re.MULTILINE)
CATEGORY_RE = re.compile(r"^category:\s*(.+)$", re.MULTILINE)

DENY = ["data/dicom_temp", "data/raw"]
SKIP_DIRS = {
    "node_modules", ".git", ".venv", "venv", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".next", "dist", "build",
    ".turbo", "coverage", ".obsidian",
}


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


mcp = FastMCP("graphify-mcp")

_STEM_CACHE: dict[str, str] | None = None


def _node_key(p: Path) -> str:
    return str(p.relative_to(VAULT_ROOT)).replace("\\", "/")


def _ensure_stem_cache() -> dict[str, str]:
    global _STEM_CACHE
    if _STEM_CACHE is None:
        cache: dict[str, str] = {}
        for md in _walk_md(VAULT_ROOT):
            if any(d in str(md) for d in DENY):
                continue
            stem = md.stem
            if stem not in cache:
                cache[stem] = _node_key(md)
        _STEM_CACHE = cache
    return _STEM_CACHE


def _invalidate_caches() -> None:
    global _STEM_CACHE
    _STEM_CACHE = None


def _resolve_link(link: str, source: Path) -> str | None:
    link = link.strip().split("#")[0]
    if not link:
        return None
    candidates = [link, link + ".md", f"{Path(link).stem}.md"]
    if source.is_relative_to(VAULT_ROOT):
        src_dir = source.parent.relative_to(VAULT_ROOT)
    else:
        src_dir = Path(".")
    for c in candidates:
        for base in [src_dir, Path(".")]:
            cand = (VAULT_ROOT / base / c).resolve()
            if cand.exists() and cand.is_file():
                return _node_key(cand)
    return _ensure_stem_cache().get(Path(link).stem)


def _build_graph() -> dict[str, Any]:
    _invalidate_caches()
    _ensure_stem_cache()
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, str]] = []
    for md in _walk_md(VAULT_ROOT):
        rel = _node_key(md)
        if any(d in rel for d in DENY):
            continue
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        fm = _parse_frontmatter(text)
        tags = _extract_tags(fm)
        category = _extract_category(fm) or (rel.split("/", 1)[0] if "/" in rel else "root")
        nodes[rel] = {
            "path": rel,
            "title": md.stem,
            "size": len(text),
            "category": category,
            "tags": tags,
        }
        seen: set[str] = set()
        for link in WIKILINK_RE.findall(text):
            tgt = _resolve_link(link, md)
            if tgt and tgt not in seen:
                edges.append({"from": rel, "to": tgt, "type": "wikilink"})
                seen.add(tgt)
        for link in MD_LINK_RE.findall(text):
            tgt = _resolve_link(link, md)
            if tgt and tgt not in seen:
                edges.append({"from": rel, "to": tgt, "type": "mdlink"})
                seen.add(tgt)
    return {
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "vault_root": str(VAULT_ROOT),
        "n_nodes": len(nodes),
        "n_edges": len(edges),
        "nodes": list(nodes.values()),
        "edges": edges,
    }


def _parse_frontmatter(text: str) -> str:
    m = FRONTMATTER_RE.match(text)
    return m.group(1) if m else ""


def _extract_tags(frontmatter: str) -> list[str]:
    m = TAGS_RE.search(frontmatter)
    if not m:
        return []
    raw = m.group(1).strip()
    if raw.startswith("[") and raw.endswith("]"):
        return [t.strip().strip('"').strip("'") for t in raw[1:-1].split(",") if t.strip()]
    if raw.startswith("-"):
        return [line.strip("- ").strip().strip('"').strip("'") for line in raw.splitlines() if line.strip().startswith("-")]
    return [raw.strip().strip('"').strip("'")]


def _extract_category(frontmatter: str) -> str | None:
    m = CATEGORY_RE.search(frontmatter)
    return m.group(1).strip().strip('"').strip("'") if m else None


def _load_or_build(force: bool = False) -> dict[str, Any]:
    if not force and LATEST.exists():
        try:
            data = json.loads(LATEST.read_text(encoding="utf-8"))
            if time.time() - LATEST.stat().st_mtime < 3600:
                return data
        except Exception:
            pass
    g = _build_graph()
    try:
        SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
        LATEST.write_text(json.dumps(g, indent=2), encoding="utf-8")
        ts = time.strftime("%Y%m%d-%H%M%S")
        (SNAPSHOT_DIR / f"snapshot-{ts}.json").write_text(
            json.dumps(g, indent=2), encoding="utf-8"
        )
    except (PermissionError, OSError):
        pass
    return g


def _adjacency(g: dict[str, Any]) -> dict[str, set[str]]:
    adj: dict[str, set[str]] = defaultdict(set)
    for e in g["edges"]:
        adj[e["from"]].add(e["to"])
        adj[e["to"]].add(e["from"])
    return adj


@mcp.tool()
def graph_snapshot(force_rebuild: bool = False) -> dict[str, Any]:
    g = _load_or_build(force_rebuild)
    return {
        "n_nodes": g["n_nodes"],
        "n_edges": g["n_edges"],
        "built_at": g["built_at"],
        "snapshot_path": "memory/graph_snapshots/latest.json",
    }


@mcp.tool()
def graph_neighbors(node: str, depth: int = 1) -> dict[str, Any]:
    g = _load_or_build()
    adj = _adjacency(g)
    if node not in adj and node not in {n["path"] for n in g["nodes"]}:
        return {"node": node, "found": False, "neighbors": []}
    seen: set[str] = {node}
    frontier: set[str] = {node}
    layers: list[list[str]] = []
    for _ in range(depth):
        nxt: set[str] = set()
        for x in frontier:
            for y in adj.get(x, ()):
                if y not in seen:
                    nxt.add(y)
                    seen.add(y)
        if not nxt:
            break
        layers.append(sorted(nxt))
        frontier = nxt
    return {"node": node, "found": True, "depth": depth, "layers": layers}


@mcp.tool()
def graph_path(from_node: str, to_node: str, max_depth: int = 6) -> dict[str, Any]:
    g = _load_or_build()
    adj = _adjacency(g)
    if from_node not in adj or to_node not in adj:
        return {"found": False, "reason": "endpoint-missing"}
    q: deque = deque([(from_node, [from_node])])
    seen = {from_node}
    while q:
        cur, path = q.popleft()
        if cur == to_node:
            return {"found": True, "path": path, "length": len(path) - 1}
        if len(path) > max_depth:
            continue
        for n in adj[cur]:
            if n not in seen:
                seen.add(n)
                q.append((n, path + [n]))
    return {"found": False, "reason": "no-path"}


@mcp.tool()
def graph_orphans() -> list[str]:
    g = _load_or_build()
    adj = _adjacency(g)
    return sorted(n["path"] for n in g["nodes"] if n["path"] not in adj or not adj[n["path"]])


@mcp.tool()
def graph_hubs(top_k: int = 10) -> list[dict[str, Any]]:
    g = _load_or_build()
    adj = _adjacency(g)
    deg = sorted(((p, len(s)) for p, s in adj.items()), key=lambda x: -x[1])
    return [{"path": p, "degree": d} for p, d in deg[:top_k]]


@mcp.tool()
def graph_export_mermaid(focus: str | None = None, depth: int = 2) -> str:
    g = _load_or_build()
    adj = _adjacency(g)
    if focus:
        seen: set[str] = {focus}
        frontier: set[str] = {focus}
        for _ in range(depth):
            nxt: set[str] = set()
            for x in frontier:
                for y in adj.get(x, ()):
                    if y not in seen:
                        nxt.add(y)
                        seen.add(y)
            frontier = nxt
        keep = seen
    else:
        keep = {n["path"] for n in g["nodes"]}
    lines = ["graph LR"]
    id_map: dict[str, str] = {}
    for i, p in enumerate(sorted(keep)):
        nid = f"n{i}"
        id_map[p] = nid
        label = Path(p).stem.replace('"', "'")[:40]
        lines.append(f'  {nid}["{label}"]')
    for e in g["edges"]:
        if e["from"] in id_map and e["to"] in id_map:
            lines.append(f"  {id_map[e['from']]} --> {id_map[e['to']]}")
    return "\n".join(lines)


@mcp.tool()
def graph_tags() -> dict[str, Any]:
    g = _load_or_build()
    counts: dict[str, int] = defaultdict(int)
    for n in g["nodes"]:
        for t in n.get("tags", []):
            counts[t] += 1
    return {"tags": dict(sorted(counts.items(), key=lambda x: -x[1])), "n_unique": len(counts)}


@mcp.tool()
def graph_by_tag(tag: str) -> list[dict[str, Any]]:
    g = _load_or_build()
    return [{"path": n["path"], "title": n["title"], "tags": n.get("tags", [])}
            for n in g["nodes"] if tag in n.get("tags", [])]


@mcp.tool()
def graph_stats() -> dict[str, Any]:
    g = _load_or_build()
    adj = _adjacency(g)
    cats: dict[str, int] = defaultdict(int)
    tag_counts: dict[str, int] = defaultdict(int)
    for n in g["nodes"]:
        cats[n["category"]] += 1
        for t in n.get("tags", []):
            tag_counts[t] += 1
    n_orphans = sum(1 for n in g["nodes"] if not adj.get(n["path"]))
    return {
        "n_nodes": g["n_nodes"],
        "n_edges": g["n_edges"],
        "n_orphans": n_orphans,
        "categories": dict(cats),
        "tags": dict(sorted(tag_counts.items(), key=lambda x: -x[1])),
        "built_at": g["built_at"],
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
