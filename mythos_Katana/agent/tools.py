"""Mock tools - no real network."""
def mock_fetch(target, mode="passive"):
    # returns redacted-safe fake data
    return {"target": target, "mode": mode, "headers": {"x-mock": "1"}, "evidence": "passive check mock"}
