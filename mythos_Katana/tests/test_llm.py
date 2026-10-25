import os

def test_llm_unconfigured_falls_back():
    os.environ.pop("KATANA_LLM_PROVIDER", None)
    from agent import llm
    assert llm.available() is False
    assert llm.ask("sys", "user") is None

def test_llm_unreachable_falls_back():
    os.environ["KATANA_LLM_PROVIDER"] = "ollama"
    os.environ["OLLAMA_HOST"] = "http://127.0.0.1:59999"
    from agent import llm
    assert llm.ask("sys", "user") is None
    os.environ.pop("KATANA_LLM_PROVIDER", None)

def test_council_debate_offline():
    os.environ.pop("KATANA_LLM_PROVIDER", None)
    from agent import persistent as P
    text, used = P.council_debate("headers_check", "HTTP/2 200")
    assert used is False
    assert "Attacker" in text and "Judge" in text
