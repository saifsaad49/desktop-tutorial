import re
from urllib.parse import urlparse

ALLOWED_SCHEMES = ("", "http", "https")

def validate_target(t, allowed_hosts=None):
    if t is None or (isinstance(t, str) and not t.strip()):
        raise ValueError("empty target: provide --target or set scope.target in config")
    t = t.strip()
    if len(t) > 253:
        raise ValueError(f"invalid target '{t}': too long")
    # reject unsupported schemes
    if "://" in t:
        scheme = t.split("://", 1)[0].lower()
        if scheme not in ALLOWED_SCHEMES:
            raise ValueError(f"unsupported scheme '{scheme}://' - use plain hostname or http(s)://")
        parsed = urlparse(t if "://" in t else "http://" + t)
        host = parsed.hostname or ""
        port = parsed.port
        # port check (urlparse raises on bad port, but double-check)
        if ":" in parsed.netloc and parsed.port is None:
            raise ValueError(f"invalid port in target '{t}'")
    else:
        # plain hostname[:port] form
        host = t.split(":")[0]
        if ":" in t:
            port_part = t.rsplit(":", 1)[1]
            if not port_part.isdigit() or not (1 <= int(port_part) <= 65535):
                raise ValueError(f"invalid port in target '{t}'")
        # hostname sanity
        if not re.match(r'^[A-Za-z0-9]([A-Za-z0-9\-\.]*[A-Za-z0-9])?$', host):
            raise ValueError(f"invalid hostname '{t}'")
    host_only = host.lower()
    if allowed_hosts is not None and host_only not in [h.lower() for h in allowed_hosts]:
        raise ValueError(f"target '{host_only}' not in allowed_hosts {allowed_hosts}")
    return t
