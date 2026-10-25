"""LLM adapter - lets the council think with a REAL model.

Enable by setting env vars (nothing is hardcoded, no keys in repo):
  KATANA_LLM_PROVIDER = anthropic | openai | ollama
  KATANA_LLM_MODEL    = model name (optional)
  ANTHROPIC_API_KEY / OPENAI_API_KEY as needed
If provider is unset or unreachable, callers fall back to offline templates.
"""
import os, json, urllib.request, urllib.error

PROVIDER = lambda: os.environ.get("KATANA_LLM_PROVIDER", "").strip().lower()
DEFAULT_MODEL = {
    "anthropic": "claude-3-5-haiku-latest",
    "openai": "gpt-4o-mini",
    "ollama": "llama3.2",
}

def _post(url, headers, payload, timeout=90):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", **headers}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

def available():
    p = PROVIDER()
    if p == "anthropic":
        return bool(os.environ.get("ANTHROPIC_API_KEY"))
    if p in ("openai", "openai-compatible", "compatible"):
        return bool(os.environ.get("OPENAI_API_KEY"))
    if p == "ollama":
        return True
    return False

def ask(system, user, max_tokens=400):
    """Return model text, or None if not configured/unreachable."""
    p = PROVIDER()
    if not available():
        return None
    model = os.environ.get("KATANA_LLM_MODEL") or DEFAULT_MODEL.get(p, "")
    try:
        if p == "anthropic":
            d = _post("https://api.anthropic.com/v1/messages",
                      {"x-api-key": os.environ["ANTHROPIC_API_KEY"],
                       "anthropic-version": "2023-06-01"},
                      {"model": model, "max_tokens": max_tokens, "system": system,
                       "messages": [{"role": "user", "content": user}]})
            return "".join(b.get("text", "") for b in d.get("content", [])) or None
        if p in ("openai", "openai-compatible", "compatible"):
            base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
            d = _post(f"{base}/chat/completions",
                      {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
                      {"model": model, "max_tokens": max_tokens,
                       "messages": [{"role": "system", "content": system},
                                    {"role": "user", "content": user}]})
            return d["choices"][0]["message"]["content"] or None
        if p == "ollama":
            base = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
            d = _post(f"{base}/api/chat", {},
                      {"model": model, "stream": False,
                       "messages": [{"role": "system", "content": system},
                                    {"role": "user", "content": user}]})
            return d.get("message", {}).get("content") or None
    except Exception:
        return None
    return None

def status():
    p = PROVIDER() or "none"
    return f"provider={p} model={os.environ.get('KATANA_LLM_MODEL') or DEFAULT_MODEL.get(p,'-')} available={available()}"
