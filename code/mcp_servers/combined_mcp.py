"""combined-mcp — Einzelner MCP-Server für Obsidian + Graphify + Hermes + Browser.

Reduziert RAM-Overhead gegenüber 4 separaten Prozessen.
Wenn ein Sub-Modul fehlt (z.B. Playwright), werden dessen Tools übersprungen.
"""
from __future__ import annotations

import os
import sys
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
os.environ["CAROTIS_VAULT_ROOT"] = str(VAULT_ROOT)

sys.path.insert(0, str(Path(__file__).parent))

mcp = FastMCP("carotis-combined")

# ── Obsidian ──
try:
    import obsidian_mcp as _obs
    mcp.add_tool(_obs.vault_read)
    mcp.add_tool(_obs.vault_write)
    mcp.add_tool(_obs.vault_search)
    mcp.add_tool(_obs.vault_backlinks)
    mcp.add_tool(_obs.vault_stats)
    print("[combined] obsidian tools loaded", file=sys.stderr)
except Exception as e:
    print(f"[combined] obsidian skipped: {e}", file=sys.stderr)

# ── Graphify ──
try:
    import graphify_mcp as _gf
    mcp.add_tool(_gf.graph_snapshot)
    mcp.add_tool(_gf.graph_neighbors)
    mcp.add_tool(_gf.graph_path)
    mcp.add_tool(_gf.graph_orphans)
    mcp.add_tool(_gf.graph_hubs)
    mcp.add_tool(_gf.graph_export_mermaid)
    mcp.add_tool(_gf.graph_stats)
    mcp.add_tool(_gf.graph_tags)
    mcp.add_tool(_gf.graph_by_tag)
    print("[combined] graphify tools loaded", file=sys.stderr)
except Exception as e:
    print(f"[combined] graphify skipped: {e}", file=sys.stderr)

# ── Hermes ──
try:
    import hermes_mcp as _hm
    mcp.add_tool(_hm.hermes_health)
    mcp.add_tool(_hm.hermes_list_skills)
    mcp.add_tool(_hm.hermes_call_skill)
    mcp.add_tool(_hm.hermes_reflect)
    mcp.add_tool(_hm.hermes_compress)
    mcp.add_tool(_hm.hermes_function_call)
    mcp.add_tool(_hm.hermes_chat)
    print("[combined] hermes tools loaded", file=sys.stderr)
except Exception as e:
    print(f"[combined] hermes skipped: {e}", file=sys.stderr)

# ── Browser ──
try:
    import browser_mcp as _br
    mcp.add_tool(_br.browser_navigate)
    mcp.add_tool(_br.browser_snapshot)
    mcp.add_tool(_br.browser_click)
    mcp.add_tool(_br.browser_type)
    mcp.add_tool(_br.browser_evaluate)
    mcp.add_tool(_br.browser_close)
    print("[combined] browser tools loaded", file=sys.stderr)
except Exception as e:
    print(f"[combined] browser skipped: {e}", file=sys.stderr)


@mcp.tool()
def combined_status() -> dict[str, Any]:
    """Health-Check für alle Sub-Module."""
    status: dict[str, Any] = {}
    try:
        import obsidian_mcp as _o
        status["obsidian"] = _o.vault_stats()
    except Exception as e:
        status["obsidian"] = {"error": str(e)}
    try:
        import graphify_mcp as _g
        status["graphify"] = _g.graph_stats()
    except Exception as e:
        status["graphify"] = {"error": str(e)}
    try:
        import hermes_mcp as _h
        status["hermes"] = _h.hermes_health()
    except Exception as e:
        status["hermes"] = {"error": str(e)}
    try:
        import browser_mcp as _b
        status["browser"] = {"playwright_ok": _b._PW_OK}
    except Exception as e:
        status["browser"] = {"error": str(e)}
    return status


if __name__ == "__main__":
    mcp.run(transport="stdio")
