import subprocess, sys
def run(*a):
    r = subprocess.run([sys.executable, "-m", "agent.loop"] + list(a), capture_output=True, text=True)
    return r
def test_no_target_fails_gracefully():
    r = run("--config", "/tmp/cfg_empty2.yaml", "--engagement", "e-x", "--mode", "passive")
    # create empty-scope config first
    assert r.returncode in (1, 2)
def test_empty_target_rejected():
    r = run("--config", "config/config.yaml", "--target", "", "--engagement", "e-x", "--mode", "passive", "--max-iterations", "1")
    assert r.returncode == 2
def test_bad_scheme_rejected():
    r = run("--config", "config/config.yaml", "--target", "ftp://example.com", "--engagement", "e-x", "--mode", "passive", "--max-iterations", "1")
    assert r.returncode == 2
def test_bad_port_rejected():
    r = run("--config", "config/config.yaml", "--target", "example.com:99999", "--engagement", "e-x", "--mode", "passive", "--max-iterations", "1")
    assert r.returncode == 2
def test_zero_iterations_rejected():
    r = run("--config", "config/config.yaml", "--target", "lab.local", "--engagement", "e-x", "--mode", "passive", "--max-iterations", "0")
    assert r.returncode == 2
def test_negative_timeout_rejected():
    r = run("--config", "config/config.yaml", "--target", "lab.local", "--engagement", "e-x", "--mode", "passive", "--timeout", "-5")
    assert r.returncode == 2
