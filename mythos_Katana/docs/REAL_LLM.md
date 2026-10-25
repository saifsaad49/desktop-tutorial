# Turning the council into a REAL thinking model

The scanner loop costs **zero tokens** by itself (pure Python + curl).
The *thinking* part (6-mind debate) can use a real model. Set one env var group:

## Option A - Anthropic (Claude)
```bash
export KATANA_LLM_PROVIDER=anthropic
export ANTHROPIC_API_KEY=sk-ant-...
export KATANA_LLM_MODEL=claude-3-5-haiku-latest   # optional
python -m agent.persistent
```

## Option B - Any OpenAI-compatible endpoint (gateway / proxy / your own plan gateway)
```bash
export KATANA_LLM_PROVIDER=openai
export OPENAI_API_KEY=...
export OPENAI_BASE_URL=https://your-gateway/v1   # optional
python -m agent.persistent
```

## Option B2 - Hosted gateway (OpenAI-compatible relay)
Works with any relay that exposes `/chat/completions`, e.g. a third-party gateway:
```bash
export KATANA_LLM_PROVIDER=openai
export OPENAI_API_KEY=<your-gateway-key>
export OPENAI_BASE_URL=https://<your-gateway>/api/v1
export KATANA_LLM_MODEL=<model-id-from-/models>
python -m agent.persistent
```
Discover model ids with:
```bash
curl -s $OPENAI_BASE_URL/models -H "Authorization: Bearer $OPENAI_API_KEY"
```

**Never commit the key.** Keep it in the environment or a file outside the repo.

## Option C - Local model (free, no token cost at all)
```bash
ollama pull llama3.2
export KATANA_LLM_PROVIDER=ollama
export KATANA_LLM_MODEL=llama3.2
python -m agent.persistent
```

## Behaviour
- If the provider is unset or unreachable, the loop **never stalls** - it falls back to offline templates.
- Each log line shows `llm=True|False` so you can see which mode produced the debate.
- Check current mode: `python -c "from agent import llm; print(llm.status())"`

## Cost control
- The 6-mind debate runs **once per round** (not 6 separate calls) - one request per round.
- Raise `time.sleep(12)` in `agent/persistent.py` to slow rounds and cut usage further.
- Run it on your own server with a local model for zero cost.
