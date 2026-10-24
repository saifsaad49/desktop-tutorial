def next_tool(history, available):
    for t in available:
        if t not in [h.get("tool") for h in history]:
            return t
    return available[0]
