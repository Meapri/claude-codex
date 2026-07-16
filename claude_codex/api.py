"""HTTP helpers for Anthropic Messages API (stdlib only)."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

from . import auth

DEFAULT_BASE = "https://api.anthropic.com"
ANTHROPIC_VERSION = "2023-06-01"


def base_url() -> str:
    return os.getenv("ANTHROPIC_BASE_URL", DEFAULT_BASE).rstrip("/")


def http_json(
    method: str,
    url: str,
    headers: Dict[str, str],
    body: Optional[Dict[str, Any]],
    timeout: float,
) -> Dict[str, Any]:
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")[:2000]
        raise RuntimeError(f"HTTP {exc.code}: {err_body}") from exc


def auth_headers() -> Dict[str, str]:
    key = auth.get_api_key()
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY is not configured")
    return {
        "x-api-key": key,
        "anthropic-version": ANTHROPIC_VERSION,
        "content-type": "application/json",
    }


def list_models_live(timeout: float = 30.0) -> List[Dict[str, Any]]:
    url = f"{base_url()}/v1/models"
    payload = http_json("GET", url, auth_headers(), None, timeout)
    items = payload.get("data") or []
    out: List[Dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        mid = str(item.get("id") or "").strip()
        if mid:
            out.append({"id": mid, "display": mid, "source": "live"})
    return out


def messages_create(body: Dict[str, Any], *, timeout: float = 120.0) -> Dict[str, Any]:
    url = f"{base_url()}/v1/messages"
    return http_json("POST", url, auth_headers(), body, timeout)
