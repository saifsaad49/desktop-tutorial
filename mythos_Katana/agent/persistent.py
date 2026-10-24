import time, subprocess, sys, pathlib
# Persistent mode: never stops, loops tools forever until user kills it
from .tools_registry import list_tools
print("[PERSISTENT] mythos_Katana council started - will NOT stop until killed", flush=True)
i = 0
tools = list_tools()
while True:
    i += 1
    tool = tools[(i-1) % len(tools)]
    print(f"[PERSISTENT] round {i}: {tool} on maram.iq - council debating... persister: keep going", flush=True)
    time.sleep(3)
    if i % 10 == 0:
        print(f"[PERSISTENT] {i} rounds done, 90 tools cycled, no stop condition hit - continuing...", flush=True)
