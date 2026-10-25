"""LLM adapter - lets the council think with a REAL model.

Enable with env vars (nothing hardcoded, no keys in the repo):
  KATANA_LLM_PROVIDER = anthropic | openai | ollama
  KATANA_LLM_MODEL    = model id (optional)
  KATANA_LLM_TIMEOUT  = seconds per attempt (default 45)
  KATANA_LLM_RETRIES  = extra attempts after the first (default 2)
  ANTHROPIC_API_KEY / OPENAI_API_KEY / OPENAI_BASE_URL as needed
If the provider is unset, slow, or failing, callers fall back to offline
templates so the scan loop never stalls.
"""
import os, json, time, urllib.request, urllib.error

DEFAULT_MODEL = {
    "anthropic": "claude-3-5-haiku-latest",
    "openai": "gpt-4o-mini",
    "ollama": "llama3.2",
}
LAST_ERROR = None

def _provider():
    return os.environ.get("KATANA_LLM_PROVIDER", "").strip().lower()

def _timeout():
    try:
        return float(os.environ.get("KATANA_LLM_TIMEOUT", "45"))
    except ValueError:
        return 45.0

def _retries():
    try:
        return int(os.environ.get("KATANA_LLM_RETRIES", "2"))
    except ValueError:
        return 2

def _post(url, headers, payload, timeout):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", **headers}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

def available():
    p = _provider()
    if p == "anthropic":
        return bool(os.environ.get("ANTHROPIC_API_KEY"))
    if p in ("openai", "openai-compatible", "compatible"):
        return bool(os.environ.get("OPENAI_API_KEY"))
    if p == "ollama":
        return True
    return False

def _attempt(system, user, max_tokens):
    p = _provider()
    model = os.environ.get("KATANA_LLM_MODEL") or DEFAULT_MODEL.get(p, "")
    if p == "anthropic":
        d = _post("https://api.anthropic.com/v1/messages",
                  {"x-api-key": os.environ["ANTHROPIC_API_KEY"],
                   "anthropic-version": "2023-06-01"},
                  {"model": model, "max_tokens": max_tokens, "system": system,
                   "messages": [{"role": "user", "content": user}]},
                  _timeout())
        return "".join(b.get("text", "") for b in d.get("content", [])) or None
    if p in ("openai", "openai-compatible", "compatible"):
        base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        d = _post(base + "/chat/completions",
                  {"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]},
                  {"model": model, "max_tokens": max_tokens,
                   "messages": [{"role": "system", "content": system},
                                {"role": "user", "content": user}]},
                  _timeout())
        return d["choices"][0]["message"]["content"] or None
    if p == "ollama":
        base = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
        d = _post(base + "/api/chat", {},
                  {"model": model, "stream": False,
                   "messages": [{"role": "system", "content": system},
                                {"role": "user", "content": user}]},
                  _timeout())
        return d.get("message", {}).get("content") or None
    return None

def ask(system, user, max_tokens=400):
    """Return model text, or None if unconfigured/failing. Never raises."""
    global LAST_ERROR
    if not available():
        LAST_ERROR = "provider not configured"
        return None
    attempts = max(1, _retries() + 1)
    for n in range(attempts):
        try:
            out = _attempt(system, user, max_tokens)
            if out:
                LAST_ERROR = None
                return out
            LAST_ERROR = "empty response"
        except Exception as e:
            LAST_ERROR = "%s: %s" % (type(e).__name__, e)
        if n < attempts - 1:
            time.sleep(2 * (n + 1))
    return None

def status():
    p = _provider() or "none"
    model = os.environ.get("KATANA_LLM_MODEL") or DEFAULT_MODEL.get(p, "-")
    return "provider=%s model=%s available=%s timeout=%ss retries=%s last_error=%s" % (
        p, model, available(), _timeout(), _retries(), LAST_ERROR)
