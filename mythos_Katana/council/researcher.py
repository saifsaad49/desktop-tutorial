from agent.tools_registry import run_tool
def research(target, history):
    # mock researcher: picks next unused tool
    for t in ["cve_lookup","headers_check","ssl_check"]:
        if not any(h.get("tool")==t for h in history):
            return run_tool(t, target)
    return run_tool("tech_fingerprint", target)
