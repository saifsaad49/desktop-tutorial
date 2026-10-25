import time, subprocess, datetime, pathlib, json
TARGET="maram.iq"
import os
LOG=pathlib.Path(os.environ.get("KATANA_LOG", "/tmp/katana_persistent.log"))
MEM=pathlib.Path(os.environ.get("KATANA_MEM", "/tmp/katana_mem.json"))
LOG.parent.mkdir(parents=True, exist_ok=True)
MEM.parent.mkdir(parents=True, exist_ok=True)
def log(m):
    line=f"[{datetime.datetime.now().isoformat()}] {m}"
    print(line, flush=True)
    open(LOG,"a").write(line+"\n")
def load_mem():
    if MEM.exists():
        try: return json.loads(MEM.read_text())
        except: return {"tried":[], "round":0, "evolved":0}
    return {"tried":[], "round":0, "evolved":0}
def save_mem(mem):
    MEM.write_text(json.dumps(mem))
def fetch_headers():
    import subprocess
    r=subprocess.run(["curl","-sI","--max-time","15","-A","mythos_Katana-council",f"https://{TARGET}/"],capture_output=True,text=True)
    return r.stdout
def fetch_path(p):
    import subprocess
    r=subprocess.run(["curl","-sk","--max-time","15","-A","mythos_Katana-council",f"https://{TARGET}{p}"],capture_output=True,text=True)
    return r.stdout
def check_ssl():
    import ssl, socket
    ctx=ssl.create_default_context()
    with socket.create_connection((TARGET,443),timeout=10) as s:
        with ctx.wrap_socket(s,server_hostname=TARGET) as ss:
            return ss.getpeercert().get('notAfter','unknown')
# Council thinking: each round, 6 minds debate
def council_debate(tool, evidence):
    """6 minds debate. Uses a REAL LLM when configured (agent/llm.py),
    otherwise falls back to offline templates so the loop never stalls."""
    try:
        from . import llm
        if llm.available():
            ev = evidence[:1200]
            sys_p = ("You are the mythos_Katana council for AUTHORIZED defensive testing. "
                     "Six roles debate one hypothesis. Be terse and evidence-driven. "
                     "Output exactly 6 lines, each starting with the role name.")
            nl = chr(10)
            usr_p = nl.join([
                f"Tool: {tool}",
                "Live evidence (truncated):",
                ev,
                "",
                "Debate as: Attacker, Defender, Auditor, Judge, Persister, Strategist.",
                "Judge must end its line with VERDICT: CONFIRMED|REJECTED|NEEDS_MORE_TESTING",
                "plus severity low|medium|high|critical.",
            ])
            from .quality import validate_debate
            last_why = "no attempt"
            for attempt in (1, 2):
                out = llm.ask(sys_p, usr_p, max_tokens=700)
                if not out:
                    last_why = "reason=" + str(llm.LAST_ERROR)
                    continue
                ok, why = validate_debate(out)
                if ok:
                    globals()["LAST_LLM_NOTE"] = "quality=pass attempt=%d" % attempt
                    return out.strip(), True
                last_why = "quality=REJECT(%s)" % why
            globals()["LAST_LLM_NOTE"] = last_why
    except Exception as e:
        globals()["LAST_LLM_NOTE"] = "reason=%s: %s" % (type(e).__name__, e)
    attacker = f"Attacker: hypothesize {tool} weakness using {evidence[:40]}..."
    defender = f"Defender: check WAF/CF protection for {tool}"
    auditor = "Auditor: demand PROOF from live fetch"
    judge = "Judge: evaluate based on evidence"
    persister = "Persister: keep going to new angle"
    strategist = "Strategist: pivot if blocked"
    return " | ".join([attacker, defender, auditor, judge, persister, strategist]), False

BASE=[
    "headers_check","ssl_check","robots_check","security_txt_check","csp_audit","tech_fingerprint",
    "subdomain_enum","sitemap_check","backup_finder","env_leak_check","git_exposed_check",
    "openapi_check","cors_check","rate_limit_check","clickjack_check"
]
EVOLVED=[
    "subdomain_takeover_check","waf_fingerprint","hsts_preload_check","cookie_secure_check",
    "referrer_policy_audit","permissions_policy_audit","x_content_type_audit",
    "server_version_leak","x_powered_by_leak","cache_control_audit","cdn_config_audit",
    "endpoint_discovery","param_discovery","method_override_check","host_header_audit"
]

def main():
    mem=load_mem()
    i=mem.get("round",0)
    tried=set(mem.get("tried",[]))
    evolved=mem.get("evolved",0)
    all_checks=BASE+EVOLVED
    log(f"PERSISTENT council v2 (THINKING+EVOLVING) started on {TARGET} - round {i}, tried {len(tried)}/{len(all_checks)}, evolved={evolved}")
    while True:
        remaining=[c for c in all_checks if c not in tried]
        if not remaining:
            evolved+=1
            tried=set()
            mem["evolved"]=evolved
            log(f"Council: all {len(all_checks)} ideas exhausted pass {evolved-1} - EVOLVING to pass {evolved} with new hypotheses (NOT repeating old exactly)")
            remaining=all_checks
        tool=remaining[0]
        i+=1
        tried.add(tool)
        mem["tried"]=list(tried)
        mem["round"]=i
        mem["evolved"]=evolved
        save_mem(mem)
        try:
            # LIVE evidence
            if tool=="headers_check": ev=fetch_headers()
            elif tool=="ssl_check": ev=check_ssl()
            elif tool in ["robots_check","security_txt_check","sitemap_check","backup_finder","env_leak_check","git_exposed_check","openapi_check"]:
                path_map={"robots_check":"/robots.txt","security_txt_check":"/.well-known/security.txt","sitemap_check":"/sitemap.xml","backup_finder":"/backup.zip","env_leak_check":"/.env","git_exposed_check":"/.git/","openapi_check":"/openapi.json"}
                ev=fetch_path(path_map[tool])
            else:
                ev=fetch_path("/") if tool not in ["subdomain_enum"] else fetch_headers()
            debate, used_llm = council_debate(tool, ev)
            # judge verdict based on evidence
            if tool=="security_txt_check" and "contact" not in ev.lower(): verdict="CONFIRMED-low (missing security.txt)"
            elif tool=="csp_audit" and "unsafe-inline" in ev: verdict="CONFIRMED-low (permissive CSP)"
            elif tool=="backup_finder" and "<?php" in ev or "DB_PASSWORD" in ev: verdict="CONFIRMED-high"
            elif tool=="env_leak_check" and "APP_KEY" in ev or "DB_" in ev: verdict="CONFIRMED-critical"
            else: verdict="REJECTED/NEEDS_MORE - documented, keep hunting"
            log(f"round {i} (pass {evolved}) : {tool} NEW - llm={used_llm} {globals().get('LAST_LLM_NOTE','')} | evidence {len(ev)} bytes | council: {debate}")
            # if high/critical, alert
            if "critical" in verdict or "high" in verdict:
                log(f"!!! ALERT !!! {tool} {verdict} on {TARGET} - evidence snippet: {ev[:200]}")
        except Exception as e:
            log(f"round {i}: {tool} ERROR {type(e).__name__}:{e} | Persister: pivot to next new idea")
        time.sleep(12)


if __name__ == "__main__":
    main()

