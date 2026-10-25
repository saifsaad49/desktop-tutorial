# Install

## Requirements
- Python 3.10+
- `pip install -r requirements.txt`

## Run directly
```bash
python -m agent.loop --config config/config.yaml \
  --target lab.local --engagement eng-001 --mode passive --max-iterations 5
```

## Run forever (persistent council)
```bash
python -m agent.persistent            # runs until Ctrl+C
nohup ./scripts/supervise.sh &        # zero-token watchdog that keeps it alive
```

## As a Skill — Claude Code
```bash
claude skills add ./mythos_Katana --name mythos_katana
claude --skill mythos_katana "review lab.local and keep going until you have evidence"
```

## As a Skill — Codex / OpenCode
```bash
codex skill install ./mythos_Katana
opencode skill add mythos_katana
```

## As a Skill — Hermes / any other model
Copy `SKILL.md` into the system prompt. No code changes needed.

## Docker
```bash
docker build -t mythos-katana .
docker run --rm mythos-katana --config config/config.yaml --target lab.local \
  --engagement eng-001 --mode passive
```

## Model configuration (optional)
See [docs/REAL_LLM.md](docs/REAL_LLM.md). Without a model the council uses
offline templates and still never stalls.
