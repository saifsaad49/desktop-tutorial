# Changelog

## 0.6.0
- Quality gate for council debates (rejects garbled / off-topic / role-less output)
- One retry before falling back to offline templates
- LLM adapter: configurable timeout, retries, 429 backoff, exact failure reason logged
- Persistent paths via `KATANA_LOG` / `KATANA_MEM` so state survives restarts
- Portable `scripts/run_persistent.sh` + zero-token `scripts/supervise.sh`
- Docs: REAL_LLM.md, RUN_FOREVER.md

## 0.5.0
- Real LLM mode (Anthropic / OpenAI-compatible / Ollama) with graceful fallback
- Council debate wired to the model, one request per round

## 0.4.0
- Memory-aware persistent scanner: 30 checks, never repeats a tried check
- 90-tool mock registry

## 0.3.0
- Graceful error handling: target validation, allowlist, friendly messages
- 8 regression tests

## 0.2.0
- Tool registry, vector memory, researcher, per-engagement reports

## 0.1.0
- Initial council skeleton (6 minds), config, loop
