"""Tool Registry - all tools are MOCKS, no real network/exploit."""
REGISTRY = {}

def tool(name):
    def deco(fn):
        REGISTRY[name]=fn
        return fn
    return deco

@tool("cve_lookup")
def cve_lookup(target, **kw): return {"tool":"cve_lookup","target":target,"mock_cves":["CVE-2024-mock-001"]}

@tool("headers_check")
def headers_check(target, **kw): return {"tool":"headers_check","missing":["X-Frame-Options"]}

@tool("ssl_check")
def ssl_check(target, **kw): return {"tool":"ssl_check","expiry_days": 88}

@tool("dns_enum")
def dns_enum(target, **kw): return {"tool":"dns_enum","records":["A 1.2.3.4"]}

@tool("whois")
def whois(target, **kw): return {"tool":"whois","registrar":"mock-registrar"}

@tool("nmap_adapter")
def nmap_adapter(target, **kw): return {"tool":"nmap","open_ports":[80,443]}

@tool("nuclei_adapter")
def nuclei_adapter(target, **kw): return {"tool":"nuclei","findings":[]}

@tool("zap_adapter")
def zap_adapter(target, **kw): return {"tool":"zap","alerts":[]}

@tool("tech_fingerprint")
def tech_fingerprint(target, **kw): return {"tool":"tech_fingerprint","stack":["nginx","python"]}

def run_tool(name, target, **kw):
    if name not in REGISTRY: return {"error": f"unknown tool {name}"}
    return REGISTRY[name](target, **kw)

def list_tools(): return list(REGISTRY.keys())
