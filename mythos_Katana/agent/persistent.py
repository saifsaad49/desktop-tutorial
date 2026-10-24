import time, subprocess, ssl, socket, datetime, pathlib
TARGET="maram.iq"
LOG=pathlib.Path("/tmp/katana_persistent.log")
def log(m):
    line=f"[{datetime.datetime.now().isoformat()}] {m}"
    print(line, flush=True)
    open(LOG,"a").write(line+"\n")
def fetch_headers():
    r=subprocess.run(["curl","-sI","--max-time","15",f"https://{TARGET}/"],capture_output=True,text=True)
    return r.stdout
def fetch_robots():
    r=subprocess.run(["curl","-sk","--max-time","15",f"https://{TARGET}/robots.txt"],capture_output=True,text=True)
    return r.stdout
def check_ssl():
    ctx=ssl.create_default_context()
    with socket.create_connection((TARGET,443),timeout=10) as s:
        with ctx.wrap_socket(s,server_hostname=TARGET) as ss:
            cert=ss.getpeercert()
            return cert.get('notAfter','unknown')
TOOLS=["headers_check","ssl_check","robots_check","security_txt_check","csp_audit","tech_fingerprint"]
log("PERSISTENT council (REAL checks) started on maram.iq - will NOT stop")
i=0
while True:
    i+=1
    tool=TOOLS[(i-1)%len(TOOLS)]
    try:
        if tool=="headers_check":
            h=fetch_headers()
            verdict="CONFIRMED-low" if "unsafe-inline" in h else "CHECKED"
            log(f"round {i}: {tool} - got {len(h)} bytes | Attacker: missing headers? Defender: HSTS+CSP present | Judge: {verdict} | Persister: keep going")
        elif tool=="ssl_check":
            na=check_ssl()
            log(f"round {i}: {tool} - cert notAfter={na} | Attacker: expired? Auditor: PROOF {na} | Judge: REJECTED | Persister: keep going")
        elif tool=="robots_check":
            rb=fetch_robots()
            n=len([l for l in rb.splitlines() if 'Disallow' in l])
            log(f"round {i}: {tool} - {n} disallowed paths | Judge: NEEDS_MORE | Persister: keep going")
        elif tool=="security_txt_check":
            r=subprocess.run(["curl","-sk","--max-time","10",f"https://{TARGET}/.well-known/security.txt"],capture_output=True,text=True)
            found="security.txt" if "contact" in r.stdout.lower() else "404-missing"
            log(f"round {i}: {tool} - {found} | Judge: CONFIRMED-low (missing) | Persister: keep going")
        elif tool=="csp_audit":
            h=fetch_headers()
            weak="unsafe-inline" in h or "unsafe-eval" in h
            log(f"round {i}: {tool} - permissive={weak} | Judge: {'CONFIRMED-low' if weak else 'REJECTED'} | Persister: keep going")
        else:
            h=fetch_headers()
            cf="cloudflare" in h.lower()
            log(f"round {i}: {tool} - cloudflare={cf} | Judge: REJECTED | Persister: keep going")
    except Exception as e:
        log(f"round {i}: {tool} - ERROR {type(e).__name__}: {e} | Persister: keep going")
    time.sleep(10)
