def test_tools_count():
    from agent.tools_registry import list_tools
    assert len(list_tools()) >= 40

def test_redact():
    from agent.redact import redact
    assert "[REDACTED]" in redact("token=abc123")
