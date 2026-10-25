from agent.quality import validate_debate

GOOD = ("Attacker: CSP lacks frame-ancestors, clickjacking risk. "
        "Defender: WAF limits exploitation. Auditor: header evidence confirmed. "
        "Judge: VERDICT: CONFIRMED severity low. Persister: continue. "
        "Strategist: harden CSP.")

def test_good_debate_passes():
    ok, why = validate_debate(GOOD)
    assert ok, why

def test_empty_rejected():
    assert validate_debate("")[0] is False

def test_offtopic_rejected():
    assert validate_debate("Attacker: pizza. Defender: pasta. Auditor: salad. "
                           "Judge: VERDICT: CONFIRMED. Persister: eat. Strategist: cook.")[0] is False

def test_error_text_rejected():
    assert validate_debate("Attacker: HTTP 429 in header check. Defender: traceback. "
                           "Auditor: cve. Judge: VERDICT: CONFIRMED. Persister: go. "
                           "Strategist: fix it now please.")[0] is False

def test_few_roles_rejected():
    assert validate_debate("Attacker: cve found in header check, high severity risk everywhere.")[0] is False
