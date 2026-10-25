"""Quality gate for council debates.

Guards against garbled / off-topic / truncated model output so that only
coherent cybersecurity reasoning reaches the report. If a debate fails the
gate, the caller falls back to the offline templates instead of logging noise.
"""

ROLES = ("attacker", "defender", "auditor", "judge", "persister", "strategist")

# domain vocabulary - at least one must appear for the debate to be on-topic
DOMAIN = (
    "cve", "vulnerab", "exploit", "header", "csp", "tls", "ssl", "hsts", "xss", "csrf",
    "sqli", "injection", "misconfig", "hardening", "severity", "risk", "exposure",
    "disclos", "waf", "cloudflare", "cert", "redirect", "authentication", "authorization",
    "cookie", "cors", "clickjack", "robots", "endpoint", "attack surface", "patch",
    "remediat", "recon", "enumerat", "fingerprint", "cipher",
)

VERDICTS = ("confirmed", "rejected", "needs_more_testing", "needs more testing")


def validate_debate(text):
    """Return (ok: bool, reason: str)."""
    if not text or not isinstance(text, str):
        return False, "empty output"
    t = text.strip()
    if len(t) < 80:
        return False, "too short (%d chars)" % len(t)
    low = t.lower()
    roles_found = [r for r in ROLES if r in low]
    if len(roles_found) < 3:
        return False, "only %d/6 roles present: %s" % (len(roles_found), ",".join(roles_found))
    if not any(k in low for k in DOMAIN):
        return False, "no cybersecurity vocabulary - off topic"
    if not any(v in low for v in VERDICTS):
        return False, "judge produced no verdict token"
    # garbled output heuristics
    if low.count("http 4") + low.count("traceback") > 0:
        return False, "error text leaked into debate"
    words = t.split()
    if len(words) > 20:
        uniq = len(set(w.lower() for w in words))
        if uniq / float(len(words)) < 0.25:
            return False, "repetitive/garbled (unique ratio %.2f)" % (uniq / float(len(words)))
    return True, "ok roles=%d" % len(roles_found)
