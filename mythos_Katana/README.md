# mythos_Katana ⚔️ — When One Mind Is Not Enough

> Six minds. One target. No stop condition until proof.

[![MIT](https://img.shields.io/badge/license-MIT-blue)](#) [![Python](https://img.shields.io/badge/python-3.10%2B-3776AB)](#) [![Tests](https://img.shields.io/badge/tests-16%20passing-brightgreen)](#) [![Lab Verified](https://img.shields.io/badge/lab-verified%20only-orange)](#) [![by nbn.life](https://img.shields.io/badge/crafted%20by-nbn.life-0a0a0a)](https://nbn.life)

**Crafted by the team at [nbn.life](https://nbn.life) — offensive research, defensive engineering.**

---

### Why we built this
Single-pass agents hallucinate. They see a 500 and call it RCE.

In real ops you do not trust one analyst — you put findings through a war-room.
mythos_Katana is that war-room as code: one executor, six reviewers, one rule —
*no finding leaves without evidence*.

### How it thinks
The executor proposes **one** hypothesis per iteration. The council tears it apart:

| Role | Job |
|---|---|
| **Attacker** | "Here's how this could break." |
| **Defender** | "Here's why it wouldn't in prod — WAF, auth, config." |
| **Auditor** | "Show me the packet. No log = no claim." |
| **Judge** | `CONFIRMED` / `REJECTED` / `NEEDS_MORE_TESTING` + severity |
| **Researcher** | pulls CVEs / docs (cached, rate-limited, respects robots.txt) |
| **Persister** | on REJECT it does not quit — pivots to plan B and re-queues |

Loop: `hypothesize → test → debate → pivot`. Every round uses a tool it has
**not tried before** (memory-backed), so it never loops the same ground.

### Quick start
```bash
git clone https://github.com/saifsaad49/desktop-tutorial.git
cd desktop-tutorial/mythos_Katana
pip install -r requirements.txt

# point it at YOUR lab — never someone else's system
python -m agent.loop --config config/config.yaml \
  --target lab.local --engagement eng-001 --mode passive --max-iterations 5
# -> reports/eng-001/report.md
```

Active mode requires explicit consent:
```bash
python -m agent.loop --config config/config.yaml --target lab.local \
  --engagement eng-002 --mode active --i-own-target --agree-risk
```

### Persistent mode — it never stops
```bash
python -m agent.persistent
```
Runs forever, cycling 30 checks and evolving to new hypotheses. Ctrl+C to stop.

### Run it forever on YOUR machine
```bash
export OPENAI_API_KEY=...        # or use Ollama locally, or leave unset
chmod +x scripts/*.sh
nohup ./scripts/supervise.sh > /dev/null 2>&1 &
```
`scripts/supervise.sh` is a **zero-token** watchdog: it restarts the scanner if it
ever dies. State lives in `.katana/` (git-ignored). Full guide: [docs/RUN_FOREVER.md](docs/RUN_FOREVER.md)

### Real LLM mode (the council actually thinks)
The scan loop itself costs **zero tokens** — it is Python + curl.
Only the debate can use a model. Point it at any OpenAI-compatible endpoint:
```bash
export KATANA_LLM_PROVIDER=openai
export OPENAI_API_KEY=...
export OPENAI_BASE_URL=https://your-gateway/api/v1   # optional
export KATANA_LLM_MODEL=your-model-id
```
If the model is unset, slow, or rate-limited, the loop **never stalls** — it falls
back to offline templates and logs the exact reason. See [docs/REAL_LLM.md](docs/REAL_LLM.md)

### Quality gate
The council output is validated before it is logged: missing roles, off-topic text,
no verdict, garbled output or leaked error text are all rejected
(`agent/quality.py`), and one retry is attempted before falling back.

### Use it as a Skill
Drop `SKILL.md` into Claude Code / Codex / OpenCode / Hermes — any model becomes
the council. See [INSTALL.md](INSTALL.md).

### What you get
- No more false positives passing as "critical"
- Every debate logged with live evidence — fully auditable
- Memory-backed: never repeats a check it already ran
- Fails safe: bad target, bad config, bad YAML, unwritable reports all exit cleanly
- 90-tool registry, 30-check persistent cycle, 16 tests

### Layout
```
agent/     loop.py persistent.py llm.py quality.py tools_registry.py validator.py memory.py ...
council/   attacker defender auditor judge researcher persister
scripts/   run_persistent.sh supervise.sh
config/    config.yaml schema.json
docs/      REAL_LLM.md RUN_FOREVER.md ARCHITECTURE.md demo.md
tests/     16 passing
```

### From nbn.life
We run this daily in our own lab. Private integrations, custom scopes, hosted
council — reach us at [nbn.life](https://nbn.life).

---

#### Security notice
Authorized lab research only. Test only assets you own or have explicit written
approval to assess. Misuse is on you — not on us, not on nbn.life.
