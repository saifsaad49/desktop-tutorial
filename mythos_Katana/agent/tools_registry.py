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
# --- Extra tools (still mocks) ---
@tool("dir_bruteforce_mock")
def dir_bruteforce_mock(t,**kw): return {"tool":"dir_bruteforce","found":[]}
@tool("param_discovery")
def param_discovery(t,**kw): return {"tool":"param_discovery","params":[]}
@tool("csrf_check")
def csrf_check(t,**kw): return {"tool":"csrf_check","protected":True}
@tool("xxe_detector_mock")
def xxe_detector_mock(t,**kw): return {"tool":"xxe_detector","note":"mock"}
@tool("ssti_detector_mock")
def ssti_detector_mock(t,**kw): return {"tool":"ssti_detector","note":"mock"}
@tool("lfi_detector_mock")
def lfi_detector_mock(t,**kw): return {"tool":"lfi_detector","note":"mock"}
@tool("rce_detector_mock")
def rce_detector_mock(t,**kw): return {"tool":"rce_detector","note":"mock detection only, no exec"}
@tool("graphql_scanner")
def graphql_scanner(t,**kw): return {"tool":"graphql","introspection":False}
@tool("waf_detector")
def waf_detector(t,**kw): return {"tool":"waf_detector","waf":"mock-waf"}
@tool("bucket_finder")
def bucket_finder(t,**kw): return {"tool":"bucket_finder","buckets":[]}
@tool("subdomain_takeover_check")
def subdomain_takeover_check(t,**kw): return {"tool":"takeover_check","vuln":False}
@tool("email_harvester_mock")
def email_harvester_mock(t,**kw): return {"tool":"email_harvester","emails":[]}
@tool("csp_analyzer")
def csp_analyzer(t,**kw): return {"tool":"csp_analyzer","issues":[]}
@tool("hsts_check")
def hsts_check(t,**kw): return {"tool":"hsts_check","enabled":True}
@tool("clickjack_check")
def clickjack_check(t,**kw): return {"tool":"clickjack","vuln":False}
@tool("backup_finder")
def backup_finder(t,**kw): return {"tool":"backup_finder","files":[]}
@tool("env_leak_check")
def env_leak_check(t,**kw): return {"tool":"env_leak","leaked":False}
@tool("git_exposed_check")
def git_exposed_check(t,**kw): return {"tool":"git_exposed","exposed":False}
@tool("openapi_scanner")
def openapi_scanner(t,**kw): return {"tool":"openapi","endpoints":[]}
@tool("rate_limit_check")
def rate_limit_check(t,**kw): return {"tool":"rate_limit","limited":True}
@tool("bruteforce_protection_check")
def bruteforce_protection_check(t,**kw): return {"tool":"bruteforce_protection","protected":True}
@tool("subdomain_brute")
def subdomain_brute(t,**kw): return {"tool":"subdomain_brute","found":[]}
@tool("host_header_injection_check")
def host_header_injection_check(t,**kw): return {"tool":"host_header","vuln":False}
@tool("http_smuggling_check")
def http_smuggling_check(t,**kw): return {"tool":"http_smuggling","vuln":False}
@tool("prototype_pollution_check")
def prototype_pollution_check(t,**kw): return {"tool":"proto_pollution","vuln":False}
@tool("dom_xss_scanner")
def dom_xss_scanner(t,**kw): return {"tool":"dom_xss","issues":[]}
@tool("saml_check")
def saml_check(t,**kw): return {"tool":"saml","issues":[]}
@tool("oauth_misconfig_check")
def oauth_misconfig_check(t,**kw): return {"tool":"oauth","misconfig":False}
@tool("websocket_scanner")
def websocket_scanner(t,**kw): return {"tool":"websocket","issues":[]}
@tool("tls_downgrade_check")
def tls_downgrade_check(t,**kw): return {"tool":"tls_downgrade","vuln":False}
@tool("cache_poisoning_check")
def cache_poisoning_check(t,**kw): return {"tool":"cache_poison","vuln":False}
@tool("request_smuggling_mock")
def request_smuggling_mock(t,**kw): return {"tool":"req_smuggling","vuln":False}
@tool("crlf_injection_check")
def crlf_injection_check(t,**kw): return {"tool":"crlf","vuln":False}
@tool("xxe_out_of_band_mock")
def xxe_out_of_band_mock(t,**kw): return {"tool":"xxe_oob","note":"mock"}
@tool("ldap_injection_mock")
def ldap_injection_mock(t,**kw): return {"tool":"ldap_injection","note":"mock"}
@tool("xpath_injection_mock")
def xpath_injection_mock(t,**kw): return {"tool":"xpath_injection","note":"mock"}
@tool("nosql_injection_mock")
def nosql_injection_mock(t,**kw): return {"tool":"nosql_injection","note":"mock"}
@tool("command_injection_mock")
def command_injection_mock(t,**kw): return {"tool":"cmd_injection","note":"mock detection only"}
@tool("file_upload_check")
def file_upload_check(t,**kw): return {"tool":"file_upload","restrictions":True}
@tool("auth_bypass_mock")
def auth_bypass_mock(t,**kw): return {"tool":"auth_bypass","note":"logic only"}
@tool("priv_esc_mock")
def priv_esc_mock(t,**kw): return {"tool":"priv_esc","note":"mock"}
@tool("business_logic_scanner")
def business_logic_scanner(t,**kw): return {"tool":"business_logic","issues":[]}
@tool("api_rate_bypass_check")
def api_rate_bypass_check(t,**kw): return {"tool":"api_rate_bypass","bypass":False}
@tool("jwt_none_alg_check")
def jwt_none_alg_check(t,**kw): return {"tool":"jwt_none","vuln":False}
@tool("open_redirect_mock2")
def open_redirect_mock2(t,**kw): return {"tool":"open_redirect2","vuln":False}
@tool("subdomain_hijack_scanner")
def subdomain_hijack_scanner(t,**kw): return {"tool":"subdomain_hijack","vuln":False}
@tool("cloud_metadata_check")
def cloud_metadata_check(t,**kw): return {"tool":"cloud_metadata","exposed":False}
@tool("container_esc_mock")
def container_esc_mock(t,**kw): return {"tool":"container_esc","note":"mock"}
@tool("k8s_misconfig_check")
def k8s_misconfig_check(t,**kw): return {"tool":"k8s_misconfig","issues":[]}
@tool("iac_scanner")
def iac_scanner(t,**kw): return {"tool":"iac","issues":[]}
@tool("sast_mock")
def sast_mock(t,**kw): return {"tool":"sast","findings":[]}
@tool("dast_mock")
def dast_mock(t,**kw): return {"tool":"dast","findings":[]}
@tool("secrets_entropy_check")
def secrets_entropy_check(t,**kw): return {"tool":"secrets_entropy","leaks":[]}
@tool("dependency_confusion_check")
def dependency_confusion_check(t,**kw): return {"tool":"dep_confusion","vuln":False}
@tool("typosquat_detector")
def typosquat_detector(t,**kw): return {"tool":"typosquat","typos":[]}
@tool("phishing_kit_detector")
def phishing_kit_detector(t,**kw): return {"tool":"phishing_kit","found":False}
@tool("malware_scanner_mock")
def malware_scanner_mock(t,**kw): return {"tool":"malware_scan","infected":False}
@tool("supply_chain_check")
def supply_chain_check(t,**kw): return {"tool":"supply_chain","issues":[]}
@tool("sbom_generator")
def sbom_generator(t,**kw): return {"tool":"sbom","components":[]}
@tool("license_compliance_check")
def license_compliance_check(t,**kw): return {"tool":"license_check","issues":[]}
@tool("privacy_headers_check")
def privacy_headers_check(t,**kw): return {"tool":"privacy_headers","missing":[]}
@tool("a11y_security_check")
def a11y_security_check(t,**kw): return {"tool":"a11y_sec","issues":[]}
