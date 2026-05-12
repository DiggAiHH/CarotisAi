from __future__ import annotations

import json
import os
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "http://localhost:8000"
TIMEOUT_SECONDS = 30
SPLASH_VERSION = "zweckbestimmung_2026-05-06"


@dataclass(frozen=True)
class HttpResponse:
    status: int
    headers: dict[str, str]
    body: bytes

    def json(self) -> Any:
        return json.loads(self.body.decode("utf-8"))


@dataclass(frozen=True)
class StepResult:
    name: str
    ok: bool
    detail: str


class Colors:
    enabled = "NO_COLOR" not in os.environ
    green = "\033[32m" if enabled else ""
    red = "\033[31m" if enabled else ""
    yellow = "\033[33m" if enabled else ""
    bold = "\033[1m" if enabled else ""
    reset = "\033[0m" if enabled else ""


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _url(base_url: str, path: str) -> str:
    return f"{base_url.rstrip('/')}/{path.lstrip('/')}"


def _http_request(
    base_url: str,
    method: str,
    path: str,
    *,
    headers: dict[str, str] | None = None,
    body: bytes | None = None,
) -> HttpResponse:
    request = Request(
        _url(base_url, path),
        data=body,
        headers=headers or {},
        method=method,
    )
    try:
        with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return HttpResponse(
                status=response.status,
                headers=dict(response.headers.items()),
                body=response.read(),
            )
    except HTTPError as exc:
        return HttpResponse(
            status=exc.code,
            headers=dict(exc.headers.items()),
            body=exc.read(),
        )
    except URLError as exc:
        raise RuntimeError(f"request failed: {exc}") from exc


def _json_request(
    base_url: str,
    method: str,
    path: str,
    *,
    api_key: str | None = None,
    payload: dict[str, Any] | None = None,
) -> HttpResponse:
    headers = {"Accept": "application/json"}
    body = None
    if api_key:
        headers["X-API-Key"] = api_key
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    return _http_request(base_url, method, path, headers=headers, body=body)


def _multipart_file_body(
    *,
    field_name: str,
    file_path: Path,
    content_type: str,
) -> tuple[bytes, str]:
    boundary = f"----carotis-smoke-{uuid.uuid4().hex}"
    file_bytes = file_path.read_bytes()
    parts = [
        f"--{boundary}\r\n".encode("ascii"),
        (
            f'Content-Disposition: form-data; name="{field_name}"; '
            f'filename="{file_path.name}"\r\n'
        ).encode("ascii"),
        f"Content-Type: {content_type}\r\n\r\n".encode("ascii"),
        file_bytes,
        b"\r\n",
        f"--{boundary}--\r\n".encode("ascii"),
    ]
    return b"".join(parts), boundary


def _upload_dicom(base_url: str, api_key: str, dicom_path: Path) -> HttpResponse:
    body, boundary = _multipart_file_body(
        field_name="file",
        file_path=dicom_path,
        content_type="application/dicom",
    )
    return _http_request(
        base_url,
        "POST",
        "/api/v1/inference/predict",
        headers={
            "Accept": "application/json",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "X-API-Key": api_key,
        },
        body=body,
    )


def _ok(name: str, detail: str) -> StepResult:
    return StepResult(name=name, ok=True, detail=detail)


def _fail(name: str, detail: str) -> StepResult:
    return StepResult(name=name, ok=False, detail=detail)


def _body_excerpt(response: HttpResponse) -> str:
    text = response.body.decode("utf-8", errors="replace").strip()
    return text[:300] if text else "<empty body>"


def step_root_health(base_url: str) -> StepResult:
    name = "GET /health/"
    response = _json_request(base_url, "GET", "/health/")
    if response.status != 200:
        return _fail(
            name, f"expected 200, got {response.status}: {_body_excerpt(response)}"
        )
    payload = response.json()
    if payload.get("status") != "ok":
        return _fail(name, f"expected status=ok, got {payload!r}")
    return _ok(name, "status=ok")


def step_versioned_health(base_url: str) -> StepResult:
    name = "GET /api/v1/health"
    response = _json_request(base_url, "GET", "/api/v1/health")
    if response.status != 200:
        return _fail(
            name, f"expected 200, got {response.status}: {_body_excerpt(response)}"
        )
    return _ok(name, "route live")


def step_inference(base_url: str, api_key: str) -> StepResult:
    name = "POST /api/v1/inference/predict"
    dicom_path = _repo_root() / "tests" / "test_data" / "real_mri" / "MR000000.dcm"
    if not dicom_path.exists():
        return _fail(name, f"missing fixture: {dicom_path}")

    response = _upload_dicom(base_url, api_key, dicom_path)
    if response.status != 200:
        return _fail(
            name, f"expected 200, got {response.status}: {_body_excerpt(response)}"
        )

    payload = response.json()
    required_keys = {"case_id", "audit_id", "captured_at", "model_version", "model_sha"}
    missing = sorted(required_keys - set(payload))
    if missing:
        return _fail(name, f"missing response keys: {missing}; payload={payload!r}")
    return _ok(name, f"case_id={payload['case_id']}")


def step_splash_get_is_post_only(base_url: str, api_key: str) -> StepResult:
    name = "GET /api/v1/audit/splash-confirmation"
    response = _json_request(
        base_url,
        "GET",
        "/api/v1/audit/splash-confirmation",
        api_key=api_key,
    )
    if response.status != 405:
        return _fail(
            name, f"expected 405, got {response.status}: {_body_excerpt(response)}"
        )
    return _ok(name, "POST-only route is live")


def step_splash_post(base_url: str, api_key: str) -> StepResult:
    name = "POST /api/v1/audit/splash-confirmation"
    response = _json_request(
        base_url,
        "POST",
        "/api/v1/audit/splash-confirmation",
        api_key=api_key,
        payload={
            "session_id": f"smoke-{uuid.uuid4().hex}",
            "role_hash": f"smoke-role-{uuid.uuid4().hex}",
            "confirmed_at": datetime.now(timezone.utc).isoformat(),
            "version": SPLASH_VERSION,
        },
    )
    if response.status != 200:
        return _fail(
            name, f"expected 200, got {response.status}: {_body_excerpt(response)}"
        )

    payload = response.json()
    if not payload.get("audit_id"):
        return _fail(name, f"missing audit_id: {payload!r}")
    if payload.get("server_mode") != "research_prototype":
        return _fail(name, f"expected research_prototype, got {payload!r}")
    return _ok(name, f"audit_id={payload['audit_id']}")


def _run_step(name: str, func) -> StepResult:
    try:
        return func()
    except Exception as exc:
        return _fail(name, str(exc))


def _print_summary(results: list[StepResult]) -> None:
    print(f"{Colors.bold}Carotis-AI full-stack smoke{Colors.reset}")
    for result in results:
        color = Colors.green if result.ok else Colors.red
        status = "PASS" if result.ok else "FAIL"
        print(f"{color}{status:<4}{Colors.reset} {result.name} - {result.detail}")

    passed = sum(1 for result in results if result.ok)
    total = len(results)
    color = Colors.green if passed == total else Colors.red
    print(f"{color}{passed}/{total} steps passed{Colors.reset}")


def main() -> int:
    base_url = os.environ.get("SMOKE_BASE_URL", DEFAULT_BASE_URL)
    api_key = os.environ.get("API_KEY")
    if not api_key:
        print(
            f"{Colors.red}FAIL{Colors.reset} API_KEY env var is required",
            file=sys.stderr,
        )
        return 2

    steps = [
        ("GET /health/", lambda: step_root_health(base_url)),
        ("GET /api/v1/health", lambda: step_versioned_health(base_url)),
        ("POST /api/v1/inference/predict", lambda: step_inference(base_url, api_key)),
        (
            "GET /api/v1/audit/splash-confirmation",
            lambda: step_splash_get_is_post_only(base_url, api_key),
        ),
        (
            "POST /api/v1/audit/splash-confirmation",
            lambda: step_splash_post(base_url, api_key),
        ),
    ]
    results = [_run_step(name, func) for name, func in steps]
    _print_summary(results)
    return 0 if all(result.ok for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
