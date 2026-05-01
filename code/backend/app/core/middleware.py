from __future__ import annotations


class SecurityHeadersMiddleware:
    """Add security headers to every response."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                headers = message.get("headers", [])
                # Convert list of tuples to mutable list
                headers_list = list(headers)
                headers_list.append([b"x-content-type-options", b"nosniff"])
                headers_list.append([b"x-frame-options", b"DENY"])
                headers_list.append([b"x-xss-protection", b"1; mode=block"])
                headers_list.append(
                    [b"referrer-policy", b"strict-origin-when-cross-origin"]
                )
                headers_list.append(
                    [b"permissions-policy", b"camera=(), microphone=(), geolocation=()"]
                )
                from app.core.config import get_settings

                csp_connect = get_settings().csp_connect_src
                headers_list.append(
                    [
                        b"content-security-policy",
                        f"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'self' {csp_connect}; frame-ancestors 'none'; base-uri 'self';".encode(),
                    ]
                )
                if scope.get("scheme") == "https":
                    headers_list.append(
                        [
                            b"strict-transport-security",
                            b"max-age=63072000; includeSubDomains; preload",
                        ]
                    )
                message["headers"] = headers_list
            await send(message)

        await self.app(scope, receive, send_with_headers)
