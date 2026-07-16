"""Anthropic API key auth (leaf). OAuth/Claude Code reuse is intentionally out of scope."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

from . import paths

API_KEY_ENV = "ANTHROPIC_API_KEY"
API_KEY_FILE = "api-key"


def api_key_path() -> Path:
    return paths.config_dir() / API_KEY_FILE


def get_api_key() -> str:
    env = os.getenv(API_KEY_ENV, "").strip()
    if env:
        return env
    path = api_key_path()
    if path.is_file():
        try:
            return path.read_text(encoding="utf-8").strip()
        except OSError:
            return ""
    return ""


def has_credentials() -> bool:
    return bool(get_api_key())


def save_api_key(key: str) -> Path:
    key = (key or "").strip()
    if not key:
        raise ValueError("api key is empty")
    path = api_key_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(key + "\n", encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass
    return path


def status() -> Dict[str, Any]:
    key = get_api_key()
    source = "none"
    if os.getenv(API_KEY_ENV, "").strip():
        source = API_KEY_ENV
    elif api_key_path().is_file() and key:
        source = str(api_key_path())
    return {
        "text": "Anthropic API key configured." if key else "No Anthropic API key.",
        "configured": bool(key),
        "credential_source": source,
        "api_key_present": bool(key),
        "api_key_prefix": (key[:7] + "…") if len(key) > 10 else ("set" if key else ""),
        "hint": f"export {API_KEY_ENV}=sk-ant-... or write {api_key_path()}",
    }
