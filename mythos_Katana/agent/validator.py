import re
def validate_target(t):
    if not t or len(t)>253: raise ValueError("invalid target")
    return t.strip()
