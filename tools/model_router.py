"""Route only to installed local coding models; never pull a model."""

import json
from urllib.parse import urlparse
from urllib.request import ProxyHandler, build_opener


def local_url(url: str) -> str:
    parsed = urlparse(url)
    if (
        parsed.scheme != "http"
        or parsed.hostname not in {"localhost", "127.0.0.1", "::1"}
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
        or parsed.path not in {"", "/"}
    ):
        raise ValueError("Ollama must use a loopback HTTP origin")
    return url.rstrip("/")


def installed_models(base_url: str) -> list[str]:
    opener = build_opener(ProxyHandler({}))
    with opener.open(local_url(base_url) + "/api/tags", timeout=10) as response:
        return [str(m["name"]) for m in json.load(response)["models"]]


def choose_model(installed: list[str], requested: str = "auto") -> str:
    if requested != "auto":
        if requested not in installed:
            raise ValueError("Requested model is not installed")
        return requested
    preferred = [
        "qwen3-coder:30b",
        "gpt-oss:20b",
        "qwen2.5-coder:3b",
        "qwen2.5-coder:1.5b-instruct",
    ]
    for name in preferred + sorted(installed):
        if name in installed and (name in preferred or "coder" in name):
            return name
    raise RuntimeError(
        "No installed coding model. See docs/ollama_agents.md; no automatic download."
    )
