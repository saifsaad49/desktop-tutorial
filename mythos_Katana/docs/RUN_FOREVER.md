# Run it forever (on your own machine)

Why it stops here: the cloud sandbox wipes `/tmp` and kills processes when the
container is recycled. Files under `/workspace` survive, running programs do not.

On **your** machine or server, nothing is wiped - so it truly never stops.

## 1. Get the code
```bash
git clone https://github.com/saifsaad49/desktop-tutorial.git
cd desktop-tutorial/mythos_Katana
```

## 2. Set your key (never commit it)
```bash
export OPENAI_API_KEY=sk-...
export OPENAI_BASE_URL=https://your-gateway/api/v1   # if not api.openai.com
export KATANA_LLM_MODEL=your-model-id
```

## 3. Start the scanner + the zero-token watchdog
```bash
chmod +x scripts/*.sh
nohup ./scripts/supervise.sh > /dev/null 2>&1 &
```

## 4. Check it
```bash
tail -f .katana/scan.log        # live rounds
tail -f .katana/supervisor.log  # restarts
```

## 5. Make it survive reboots (Linux, optional)
```bash
crontab -e
# add:
@reboot cd /path/to/mythos_Katana && nohup ./scripts/supervise.sh > /dev/null 2>&1 &
```

State lives in `.katana/` (log + memory) and is git-ignored, so the key never
reaches the repository.
