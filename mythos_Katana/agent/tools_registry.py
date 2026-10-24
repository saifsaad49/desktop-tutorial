"""Comprehensive Tool Registry - ALL MOCKS, no real network/exploit/payload."""
REGISTRY={}
def tool(name):
    def deco(fn):
        REGISTRY[name]=fn; return fn
    return deco

# --- Recon & OSINT ---
@tool("cve_lookup")
def cve_lookup(t,**kw): return {"tool":"cve_lookup","target":t,"mock_cves":["CVE-2024-mock-001"]}
@tool("headers_check")
def headers_check(t,**kw): return {"tool":"headers_check","missing":["X-Frame-Options","CSP"]}
@tool("ssl_check")
def ssl_check(t,**kw): return {"tool":"ssl_check","expiry_days":88,"issuer":"mock-ca"}
@tool("dns_enum")
def dns_enum(t,**kw): return {"tool":"dns_enum","records":["A 1.2.3.4"]}
@tool("whois")
def whois(t,**kw): return {"tool":"whois","registrar":"mock-registrar"}
@tool("subdomain_enum")
def subdomain_enum(t,**kw): return {"tool":"subdomain_enum","subs":[f"api.{t}"]}
@tool("tech_fingerprint")
def tech_fingerprint(t,**kw): return {"tool":"tech_fingerprint","stack":["nginx","python"]}
@tool("wayback_lookup")
def wayback_lookup(t,**kw): return {"tool":"wayback","urls":[f"https://{t}/old"]}
@tool("shodan_lookup")
def shodan_lookup(t,**kw): return {"tool":"shodan","ports":[80,443]}

# --- Network & Infra ---
@tool("nmap_adapter")
def nmap_adapter(t,**kw): return {"tool":"nmap","open_ports":[80,443]}
@tool("masscan_adapter")
def masscan_adapter(t,**kw): return {"tool":"masscan","open_ports":[80]}
@tool("nuclei_adapter")
def nuclei_adapter(t,**kw): return {"tool":"nuclei","findings":[]}
@tool("zap_adapter")
def zap_adapter(t,**kw): return {"tool":"zap","alerts":[]}
@tool("nikto_adapter")
def nikto_adapter(t,**kw): return {"tool":"nikto","checks":[]}
@tool("sslyze_adapter")
def sslyze_adapter(t,**kw): return {"tool":"sslyze","weak_ciphers":[]}
@tool("testssl_adapter")
def testssl_adapter(t,**kw): return {"tool":"testssl","grade":"A"}

# --- Web & API ---
@tool("crawler")
def crawler(t,**kw): return {"tool":"crawler","pages":[f"https://{t}/"]}
@tool("api_fuzzer_mock")
def api_fuzzer_mock(t,**kw): return {"tool":"api_fuzzer","note":"mock only - no payload sent"}
@tool("jwt_check")
def jwt_check(t,**kw): return {"tool":"jwt_check","issues":[]}
@tool("cors_check")
def cors_check(t,**kw): return {"tool":"cors_check","misconfig":False}
@tool("sqli_detector_mock")
def sqli_detector_mock(t,**kw): return {"tool":"sqli_detector","note":"detection via error patterns only, no injection"}
@tool("xss_detector_mock")
def xss_detector_mock(t,**kw): return {"tool":"xss_detector","note":"dom analysis only, no payload"}
@tool("idor_detector_mock")
def idor_detector_mock(t,**kw): return {"tool":"idor_detector","note":"logic check only"}
@tool("open_redirect_check")
def open_redirect_check(t,**kw): return {"tool":"open_redirect","vuln":False}
@tool("ssrf_detector_mock")
def ssrf_detector_mock(t,**kw): return {"tool":"ssrf_detector","note":"mock"}

# --- Cloud & Secrets ---
@tool("s3_bucket_check")
def s3_bucket_check(t,**kw): return {"tool":"s3_check","public":False}
@tool("secret_scanner")
def secret_scanner(t,**kw): return {"tool":"secret_scanner","secrets_found":0}
@tool("dependency_check")
def dependency_check(t,**kw): return {"tool":"dependency_check","vulns":[]}

def run_tool(name,target,**kw):
    return REGISTRY.get(name, lambda t,**k: {"error":"unknown"})(target,**kw)
def list_tools(): return list(REGISTRY.keys())
