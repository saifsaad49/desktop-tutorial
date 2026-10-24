# Install as Skill

## Claude Code
```bash
claude skills add ./mythos_Katana --name mythos_katana
claude --skill mythos_katana "scan lab.local" 
```

## Codex / OpenCode
```bash
codex skill install ./mythos_Katana
opencode skill add mythos_katana
```

## Hermes / Any LLM
Copy `SKILL.md` into system prompt. Works with any model.

## Manual
```bash
pip install -r requirements.txt
python -m agent.loop --config config/config.yaml --target lab.local --engagement eng-001 --i-own-target --agree-risk
```
