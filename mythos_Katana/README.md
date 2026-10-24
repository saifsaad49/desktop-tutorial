# mythos_Katana ⚔️ — The Council That Never Sleeps

> **Persistent Autonomous Cyber Council.** 6 AI minds debating in a loop — Think → Act → Observe → Persist — until truth emerges.

![license](https://img.shields.io/badge/license-MIT-blue) ![python](https://img.shields.io/badge/python-3.10%2B-green) ![scope](https://img.shields.io/badge/scope-sandbox--verified-orange) ![builtby](https://img.shields.io/badge/built%20by-nbn.life-black)

**Built & Maintained by [nbn.life](https://nbn.life) — All rights reserved. Continuous updates & enterprise support.**

---

## ⚡ The Power Concept
Most agents answer once and stop. **mythos_Katana never stops.**

A single executor agent is linked to a **Council of 6** that critiques every finding:
- **Attacker** proposes one hypothesis
- **Defender** tries to falsify it
- **Auditor** demands proof (logs/responses)
- **Judge** rules: CONFIRMED / REJECTED / NEEDS_MORE_TESTING
- **Researcher** does smart OSINT (max 3 queries/iteration, cached, respects robots.txt)
- **Persister-Strategist** prevents halt — suggests alternative path B on failure

Result: **Zero hallucination, maximum persistence.** Inspired by the Mythos "never-stop-thinking" philosophy, engineered for defensive research.

## 🚀 Quick Start
```bash
git clone https://github.com/saifsaad49/desktop-tutorial.git
cd mythos_Katana
pip install -r requirements.txt
# Set your AUTHORIZED lab target only
nano config/config.yaml
python agent/loop.py --config config/config.yaml
# Report auto-generated: reports/final_report.md
```

## 🧠 Skill Mode
Copy `SKILL.md` into any LLM (Claude / Cursor / Windsurf) — it instantly becomes a Katana Council.

## 📊 Example Output
```
Iteration 1: Hypothesis → Council: NEEDS_MORE_TESTING → Researcher fetches CVE
Iteration 2: New evidence → Judge: REJECTED (no proof)
Iteration 3: Persister pivots to path B → Judge: CONFIRMED
Report saved to reports/final_report.md
```

## 🏢 Enterprise
Updates, custom scopes, and private lab integration — contact us at **https://nbn.life**

---

### 🛡️ Security & Ethics Notice
This project is for **authorized defensive research and education in isolated Sandbox/Lab environments only**. Use only on systems you own or have explicit written permission to test. The authors and nbn.life assume no liability for misuse.
