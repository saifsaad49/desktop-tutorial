import re
PATTERNS=[r'token[=:][^\s]+',r'cookie[=:][^\s]+',r'Bearer [A-Za-z0-9\\-_\\.]+',r'secret[=:][^\s]+']
def redact(text):
    for p in PATTERNS:
        text=re.sub(p,'[REDACTED]',text, flags=re.I)
    return text
