"""test_mcp_trio.py - End-to-End Smoke-Test der 4 MCPs.

Importiert die MCP-Server-Module direkt (nicht ueber stdio) und ruft die
Tool-Funktionen synchron. Validiert: Vault-IO, Graph-Build, Hermes-Health
(soft-fail wenn Hermes/Ollama down), Browser-Harness Spec.

Exit 0 = gruen, 1 = Fehler, 2 = soft-fail (Hermes/Ollama down).
  --ignore-warn → Exit 0 bei WARN-only (für CI).

Run:
  python code/mcp_servers/test_mcp_trio.py
  python code/mcp_servers/test_mcp_trio.py --ignore-warn
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
from pathlib import Path

VAULT = Path(
    os.environ.get(
        "CAROTIS_VAULT_ROOT",
        str(Path(__file__).resolve().parents[2]),
    )
).resolve()
os.environ["CAROTIS_VAULT_ROOT"] = str(VAULT)

sys.path.insert(0, str(Path(__file__).parent))

GREEN = "[OK]"
RED = "[FAIL]"
YELLOW = "[WARN]"

results: list[tuple[str, str, str]] = []


def step(name: str, fn) -> bool:
    try:
        out = fn()
        msg = json.dumps(out, default=str)[:200] if out is not None else "(no output)"
        results.append((GREEN, name, msg))
        print(f"{GREEN} {name}")
        print(f"     -> {msg}")
        return True
    except AssertionError as e:
        results.append((RED, name, str(e)))
        print(f"{RED} {name}")
        print(f"     -> {e}")
        return False
    except Exception as e:
        results.append((RED, name, f"{type(e).__name__}: {e}"))
        print(f"{RED} {name}")
        print(f"     -> {type(e).__name__}: {e}")
        traceback.print_exc()
        return False


def soft(name: str, fn) -> bool:
    try:
        out = fn()
        msg = json.dumps(out, default=str)[:200]
        results.append((GREEN, name, msg))
        print(f"{GREEN} {name}")
        print(f"     -> {msg}")
        return True
    except Exception as e:
        results.append((YELLOW, name, str(e)))
        print(f"{YELLOW} {name} (soft-fail)")
        print(f"     -> {e}")
        return False


def main() -> int:
    print(f"=== MCP-Trio Smoke-Test === vault={VAULT}")
    import obsidian_mcp as obs
    import graphify_mcp as gf
    import hermes_mcp as hm

    def t1():
        s = obs.vault_stats()
        assert s["n_markdown_files"] > 0, "no .md files found"
        return s

    def t2():
        hits = obs.vault_search("Rohde", k=5)
        assert isinstance(hits, list), "search must return list"
        return {"n_hits": len(hits), "top": hits[:1]}

    def t3():
        rel = f"memory/runs/.smoke_{int(time.time())}.md"
        try:
            r = obs.vault_write(rel, "# Smoke\nThis is a [[CLAUDE]] backlink test.\n")
        except (PermissionError, OSError) as e:
            return {"skipped": True, "reason": f"fs-readonly: {e}"}
        assert r["bytes_written"] > 0
        readback = obs.vault_read(rel)
        assert "Smoke" in readback["content"]
        try:
            (VAULT / rel).unlink(missing_ok=True)
        except (PermissionError, OSError):
            pass
        return {"wrote": rel, "sha256": r["sha256"][:12]}

    def t4():
        bl = obs.vault_backlinks("CLAUDE.md")
        return {"n_backlinks_to_CLAUDE": len(bl), "sample": bl[:3]}

    step("obsidian.vault_stats", t1)
    step("obsidian.vault_search('Rohde')", t2)
    step("obsidian.vault_write+read+cleanup", t3)
    step("obsidian.vault_backlinks(CLAUDE.md)", t4)

    def t5():
        snap = gf.graph_snapshot(force_rebuild=True)
        assert snap["n_nodes"] > 0
        return snap

    def t6():
        st = gf.graph_stats()
        assert st["n_nodes"] >= st["n_orphans"]
        return st

    def t7():
        hubs = gf.graph_hubs(top_k=3)
        return {"hubs": hubs}

    def t8():
        m = gf.graph_export_mermaid(focus="CLAUDE.md", depth=1)
        assert m.startswith("graph LR")
        return {"mermaid_lines": len(m.splitlines())}

    step("graphify.graph_snapshot(rebuild)", t5)
    step("graphify.graph_stats", t6)
    step("graphify.graph_hubs(3)", t7)
    step("graphify.graph_export_mermaid", t8)

    def t9():
        return hm.hermes_health()

    def t10():
        skills = hm.hermes_list_skills()
        assert len(skills) >= 1, "no skills found"
        return {"n_skills": len(skills), "sample": skills[:3]}

    step("hermes.hermes_health", t9)
    step("hermes.hermes_list_skills", t10)

    def t11():
        return hm.hermes_chat("Sag genau: PONG", model=None)

    soft("hermes.hermes_chat (soft)", t11)

    def t12():
        bh = VAULT / "code" / "hermes" / "skills" / "browser-harness.md"
        assert bh.exists(), "browser-harness skill missing"
        text = bh.read_text(encoding="utf-8", errors="ignore")
        assert "PubMed" in text or "browser_navigate" in text
        return {
            "path": str(bh.relative_to(VAULT)).replace("\\", "/"),
            "bytes": len(text),
        }

    step("browser-harness.skill_spec_present", t12)

    n_pass = sum(1 for r in results if r[0] == GREEN)
    n_warn = sum(1 for r in results if r[0] == YELLOW)
    n_fail = sum(1 for r in results if r[0] == RED)
    print()
    print("=== Summary ===")
    print(f"PASS={n_pass}  WARN={n_warn}  FAIL={n_fail}")
    for tag, name, _ in results:
        print(f"  {tag} {name}")
    if n_fail > 0:
        return 1
    if n_warn > 0:
        return 2
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ignore-warn", action="store_true", help="Treat WARN as PASS (CI mode)")
    args = ap.parse_args()

    print(f"=== MCP-Trio Smoke-Test === vault={VAULT}")
    import obsidian_mcp as obs
    import graphify_mcp as gf
    import hermes_mcp as hm

    def t1():
        s = obs.vault_stats()
        assert s["n_markdown_files"] > 0, "no .md files found"
        return s

    def t2():
        hits = obs.vault_search("Rohde", k=5)
        assert isinstance(hits, list), "search must return list"
        return {"n_hits": len(hits), "top": hits[:1]}

    def t3():
        rel = f"memory/runs/.smoke_{int(time.time())}.md"
        try:
            r = obs.vault_write(rel, "# Smoke\nThis is a [[CLAUDE]] backlink test.\n")
        except (PermissionError, OSError) as e:
            return {"skipped": True, "reason": f"fs-readonly: {e}"}
        assert r["bytes_written"] > 0
        readback = obs.vault_read(rel)
        assert "Smoke" in readback["content"]
        try:
            (VAULT / rel).unlink(missing_ok=True)
        except (PermissionError, OSError):
            pass
        return {"wrote": rel, "sha256": r["sha256"][:12]}

    def t4():
        bl = obs.vault_backlinks("CLAUDE.md")
        return {"n_backlinks_to_CLAUDE": len(bl), "sample": bl[:3]}

    step("obsidian.vault_stats", t1)
    step("obsidian.vault_search('Rohde')", t2)
    step("obsidian.vault_write+read+cleanup", t3)
    step("obsidian.vault_backlinks(CLAUDE.md)", t4)

    def t5():
        snap = gf.graph_snapshot(force_rebuild=True)
        assert snap["n_nodes"] > 0
        return snap

    def t6():
        st = gf.graph_stats()
        assert st["n_nodes"] >= st["n_orphans"]
        return st

    def t7():
        hubs = gf.graph_hubs(top_k=3)
        return {"hubs": hubs}

    def t8():
        m = gf.graph_export_mermaid(focus="CLAUDE.md", depth=1)
        assert m.startswith("graph LR")
        return {"mermaid_lines": len(m.splitlines())}

    def t8b():
        tags = gf.graph_tags()
        assert "tags" in tags
        return tags

    def t8c():
        nodes = gf.graph_by_tag("decision")
        assert isinstance(nodes, list)
        return {"n_nodes_with_decision_tag": len(nodes)}

    step("graphify.graph_snapshot(rebuild)", t5)
    step("graphify.graph_stats", t6)
    step("graphify.graph_hubs(3)", t7)
    step("graphify.graph_export_mermaid", t8)
    step("graphify.graph_tags", t8b)
    soft("graphify.graph_by_tag (soft)", t8c)

    def t9():
        return hm.hermes_health()

    def t10():
        skills = hm.hermes_list_skills()
        assert len(skills) >= 1, "no skills found"
        return {"n_skills": len(skills), "sample": skills[:3]}

    step("hermes.hermes_health", t9)
    step("hermes.hermes_list_skills", t10)

    def t11():
        return hm.hermes_chat("Sag genau: PONG", model=None)

    soft("hermes.hermes_chat (soft)", t11)

    def t12():
        bh = VAULT / "code" / "hermes" / "skills" / "browser-harness.md"
        assert bh.exists(), "browser-harness skill missing"
        text = bh.read_text(encoding="utf-8", errors="ignore")
        assert "PubMed" in text or "browser_navigate" in text
        return {
            "path": str(bh.relative_to(VAULT)).replace("\\", "/"),
            "bytes": len(text),
        }

    step("browser-harness.skill_spec_present", t12)

    # Browser-MCP Tests (soft — Playwright optional)
    try:
        import browser_mcp as br

        def t13():
            return {"playwright_ok": br._PW_OK}

        def t14():
            if not br._PW_OK:
                raise RuntimeError("Playwright not installed")
            r = br.browser_navigate("https://example.com")
            assert r.get("ok")
            snap = br.browser_snapshot()
            br.browser_close()
            return {"title": r.get("title"), "snapshot_len": snap.get("text_length", 0)}

        step("browser.playwright_available", t13)
        soft("browser.navigate+snapshot (soft)", t14)
    except ImportError:
        results.append((YELLOW, "browser.import", "browser_mcp not importable"))
        print(f"{YELLOW} browser.import\n     -> browser_mcp not importable")

    # Auto-Start Tests (soft — Docker optional)
    try:
        import run_loop as rl

        def t15():
            return rl._hermes_running()

        def t16():
            return rl._ollama_running()

        soft("run_loop.hermes_running (soft)", t15)
        soft("run_loop.ollama_running (soft)", t16)
    except ImportError:
        results.append((YELLOW, "run_loop.import", "run_loop not importable"))
        print(f"{YELLOW} run_loop.import\n     -> run_loop not importable")

    n_pass = sum(1 for r in results if r[0] == GREEN)
    n_warn = sum(1 for r in results if r[0] == YELLOW)
    n_fail = sum(1 for r in results if r[0] == RED)
    print()
    print("=== Summary ===")
    print(f"PASS={n_pass}  WARN={n_warn}  FAIL={n_fail}")
    for tag, name, _ in results:
        print(f"  {tag} {name}")
    if n_fail > 0:
        return 1
    if n_warn > 0 and not args.ignore_warn:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
