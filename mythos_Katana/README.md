# mythos_Katana ⚔️ — When One Mind Is Not Enough
[![trending](https://img.shields.io/badge/trending-cybersecurity-red)]() [![stars](https://img.shields.io/github/stars/saifsaad49/desktop-tutorial)]()

> Six minds. One target. No stop condition until proof.

[![MIT](https://img.shields.io/badge/license-MIT-blue)](#) [![Python](https://img.shields.io/badge/python-3.10%2B-3776AB)](#) [![Lab Verified](https://img.shields.io/badge/lab-verified%20only-orange)](#) [![by nbn.life](https://img.shields.io/badge/crafted%20by-nbn.life-0a0a0a)](https://nbn.life)

**Crafted by the team at [nbn.life](https://nbn.life) — Offensive research, defensive engineering. We ship updates weekly.**

---

### Why we built this
Single-pass agents hallucinate. They see a 500 error and call it RCE.

In real ops, you don't trust one analyst. You put findings through a war-room.

mythos_Katana is that war-room as code: one executor, six reviewers, one rule — *no finding leaves without evidence*.

### How it thinks
The executor proposes **one** hypothesis per iteration. The council tears it apart:

**Attacker** → "Here's how this could break."  
**Defender** → "Here's why it wouldn't in prod — WAF, auth, config."  
**Auditor** → "Show me the packet. No log = no claim."  
**Judge** → `CONFIRMED | REJECTED | NEEDS_MORE_TESTING`  
**Researcher** → pulls CVEs/docs (cached, 3 queries max/iter, respects robots.txt)  
**Persister** → on REJECT, doesn't quit — pivots to Plan B and re-queues.

Loop: `hypothesize → test (passive by default) → debate → pivot`. Stops only on `CONFIRMED` or `max_iterations`.

Built after watching Mythos-style persistent reasoning and asking: *what if that persistence was auditable?*

### Quick start — lab only
```bash
git clone https://github.com/saifsaad49/desktop-tutorial.git
cd desktop-tutorial/mythos_Katana
pip install -r requirements.txt

# point it at YOUR lab — not the internet
vim config/config.yaml  # scope.target: lab.local

python agent/loop.py --config config/config.yaml
# → reports/final_report.md
```

### Use it as a Skill
Drop `SKILL.md` into Claude / Cursor / Windsurf. Any model becomes the council. No code change.

### What you get
- No more false positives passing as "critical"
- Full trace: every debate logged to `reports/`
- Tunable persistence: `max_iterations`, `backtrack_on_failure`
- Safe by default: `allow_active_scan: false`

### From nbn.life
We run this daily in our own sandbox. If you want private integrations, custom scopes, or hosted council — reach us at [nbn.life](https://nbn.life).

---

#### Security notice
Authorized lab research only. Test only assets you own or have explicit written approval to assess. Misuse is on you — not on us, not on nbn.life.
