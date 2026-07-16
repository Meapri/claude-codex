# SOURCE_MAP — Claude Codex ← Hermes

Independent Codex leaf plugin. Not Hermes. Protocol ideas only.

| Hermes source | This plugin | What was taken |
| --- | --- | --- |
| `agent/transports/anthropic.py` | `claude_codex/chat.py` | Messages API as transport; system vs messages split |
| `agent/anthropic_adapter.py` | `claude_codex/chat.py` | OpenAI→Anthropic message merge; tools → `input_schema` |
| Provider docs (API key path) | `claude_codex/auth.py` | `ANTHROPIC_API_KEY` first-class auth |
| — | intentionally omitted | Full AIAgent loop, Claude Code OAuth spoofing, gateway, memory, cron |

## Not ported (on purpose)

- Claude Max OAuth / Claude Code credential store coupling
- Adaptive thinking / beta header matrix (can be added later)
- Hermes plugin loader / config.yaml model wizard
