"""browser-mcp — Playwright-basierter Browser-MCP (Carotis-AI).

Tools:
- browser_navigate(url) → title, url
- browser_snapshot() → accessibility tree als Text
- browser_click(selector) → geklicktes Element
- browser_type(selector, text) → eingegebener Text
- browser_evaluate(js) → JavaScript-Ergebnis
- browser_close() → Browser schließen

Optional: Wenn Playwright nicht installiert → alle Tools geben Fehler zurück.
"""
from __future__ import annotations

import json
import os
import re
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as e:
    raise SystemExit("fastmcp missing. pip install mcp") from e

try:
    from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
    _PW_OK = True
except ImportError:
    _PW_OK = False
    Browser = BrowserContext = Page = Any  # type: ignore[misc,assignment]

mcp = FastMCP("browser-mcp")

# Singleton-State
_playwright: Any = None
_browser: Browser | None = None
_context: BrowserContext | None = None
_page: Page | None = None

URL_RE = re.compile(r"^https?://")


def _ensure_page() -> Page:
    if not _PW_OK:
        raise RuntimeError(
            "Playwright not installed. Run: pip install playwright>=1.40 && playwright install chromium"
        )
    global _playwright, _browser, _context, _page
    if _page is None or _page.is_closed():
        _playwright = sync_playwright().start()
        _browser = _playwright.chromium.launch(headless=True)
        _context = _browser.new_context(viewport={"width": 1280, "height": 720})
        _page = _context.new_page()
    return _page


def _safe_url(url: str) -> str:
    url = url.strip()
    if not URL_RE.match(url):
        raise ValueError(f"Only http/https URLs allowed, got: {url}")
    return url


@mcp.tool()
def browser_navigate(url: str) -> dict[str, Any]:
    """Navigate to a URL and return page metadata."""
    url = _safe_url(url)
    page = _ensure_page()
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    return {
        "url": page.url,
        "title": page.title(),
        "ok": True,
    }


@mcp.tool()
def browser_snapshot() -> dict[str, Any]:
    """Return accessibility snapshot of current page."""
    if not _PW_OK or _page is None or _page.is_closed():
        return {"error": "No page open. Call browser_navigate first."}
    try:
        # Use Playwright's accessibility tree
        tree = _page.accessibility.snapshot()
        text = _snapshot_to_text(tree)
        return {
            "url": _page.url,
            "title": _page.title(),
            "text": text[:4000],  # truncate for LLM context
            "text_length": len(text),
        }
    except Exception as e:
        return {"error": str(e)}


def _snapshot_to_text(node: dict[str, Any], depth: int = 0) -> str:
    """Flatten accessibility tree to plain text."""
    out: list[str] = []
    role = node.get("role", "")
    name = node.get("name", "")
    if name:
        indent = "  " * depth
        out.append(f"{indent}- {role}: {name}")
    for child in node.get("children", []):
        out.append(_snapshot_to_text(child, depth + 1))
    return "\n".join(out)


@mcp.tool()
def browser_click(selector: str) -> dict[str, Any]:
    """Click an element by CSS selector or text."""
    page = _ensure_page()
    try:
        page.click(selector, timeout=10000)
        return {"clicked": selector, "ok": True}
    except Exception as e:
        return {"error": str(e), "selector": selector}


@mcp.tool()
def browser_type(selector: str, text: str, submit: bool = False) -> dict[str, Any]:
    """Type text into an input field."""
    page = _ensure_page()
    try:
        page.fill(selector, text, timeout=10000)
        if submit:
            page.press(selector, "Enter")
        return {"typed": text, "selector": selector, "submitted": submit, "ok": True}
    except Exception as e:
        return {"error": str(e), "selector": selector}


@mcp.tool()
def browser_evaluate(js: str) -> dict[str, Any]:
    """Execute JavaScript in the page context."""
    page = _ensure_page()
    try:
        result = page.evaluate(js)
        return {"result": json.dumps(result, default=str)[:2000], "ok": True}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def browser_close() -> dict[str, Any]:
    """Close browser and release resources."""
    global _playwright, _browser, _context, _page
    try:
        if _context:
            _context.close()
            _context = None
        if _browser:
            _browser.close()
            _browser = None
        if _playwright:
            _playwright.stop()
            _playwright = None
        _page = None
        return {"closed": True}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run(transport="stdio")
