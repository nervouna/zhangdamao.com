Title: Configuring OpenClaw: Multi-Agent Setup, Context Management, and Memory Search
Date: 2026-04-01
Slug: configuring-openclaw-multi-agent-setup
Category: Coding
Tags: OpenClaw, LLM, Agent, Context Management, Memory Search, Ollama
Summary: A practical guide to setting up OpenClaw with multiple agents, context pruning, subagent delegation rules, and local memory search using Ollama embeddings.

I've been running [OpenClaw](https://github.com/openclaw/openclaw) for a few days now. It's powerful out of the box, but the default configuration left me with a few problems: Feishu group messages silently dropped, cron jobs failing to deliver, and sessions getting blown up by massive tool outputs. Here's what I did to fix it.

## The Setup

Three agents, each bound to a different Feishu account:

- **二毛 (main)** — my primary assistant
- **三毛 (sanmao)** — food planner, industry research
- **四毛 (simao)** — DevOps and frontend tasks

All running on MiniMax M2.7 via OAuth, with Ollama as a local fallback.

## Fixing Feishu Channel Issues

### Group messages silently dropped

The `groupPolicy` was set to `allowlist` but no `groupAllowFrom` was configured. Every group message was being discarded without any error.

Fix: set `groupPolicy` to `"open"` at both the top-level and per-account:

```json
"channels": {
  "feishu": {
    "groupPolicy": "open",
    "accounts": {
      "main": { "groupPolicy": "open" },
      "sanmao": { "groupPolicy": "open" },
      "simao": { "groupPolicy": "open" }
    }
  }
}
```

### Cron job delivery failures

Cron jobs require an explicit `delivery.to` field for Feishu. Without it, you get:

> Delivering to Feishu requires target <chatId|user:openId|chat:chatId>

Fix via CLI:

```bash
openclaw cron edit <job-id> \
  --to "user:ou_XXXXXXXXXXXXXXXXXXXXXXXXXX" \
  --channel feishu \
  --announce \
  --best-effort-deliver
```

## Context Management: Preventing Session Blowups

This was my biggest pain point. Web research, large file reads, and recursive commands would dump tens of thousands of tokens into the session, making it unusable.

### Layer 1: Context Pruning

Automatically trims old tool outputs based on time and size:

```json
"agents": {
  "defaults": {
    "contextPruning": {
      "mode": "cache-ttl",
      "ttl": "30m",
      "softTrim": {
        "maxChars": 8000,
        "headChars": 2000,
        "tailChars": 1000
      },
      "hardClear": {
        "enabled": true,
        "placeholder": "[内容已截断]"
      }
    }
  }
}
```

- `ttl: "30m"` — tool results older than 30 minutes get pruned
- `softTrim` — any single result over 8000 chars gets truncated, keeping 2000 chars from the head and 1000 from the tail
- `hardClear` — if pruning still can't bring context under control, old results get replaced with a placeholder

### Layer 2: Compaction

When the context window is nearly full, OpenClaw automatically compresses the conversation history:

```json
"compaction": {
  "mode": "safeguard",
  "maxHistoryShare": 0.5,
  "reserveTokens": 8000,
  "keepRecentTokens": 4000
}
```

- `safeguard` mode is more aggressive about protecting the session
- History never exceeds 50% of the context window
- 8000 tokens reserved for the model's response
- 4000 most recent tokens kept verbatim

### Layer 3: Subagent Delegation

For tasks known to produce massive output, I added rules to each agent's `TOOLS.md` telling them to spawn subagents instead of executing directly. A subagent runs in its own isolated session — the huge output stays there, and the parent only gets back a summary.

Rules written into `workspace/TOOLS.md`:

- **Must spawn subagent**: web research, large file reads (>200 lines), recursive commands, multi-step analysis
- **Do it directly**: single-line commands, short file reads (<50 lines), simple config changes

This is a prompt-level rule, not a config-level enforcement. But it works well in practice.

## Memory Search with Ollama

OpenClaw supports semantic memory search — querying past conversations and notes by meaning rather than keyword matching. It needs an embedding provider.

### Why Ollama

The default `local` option requires `node-llama-cpp`, which takes forever to install via npm. I already had Ollama running locally, and OpenClaw has native support for it.

### Setup

Pull an embedding model:

```bash
ollama pull qwen3-embedding:8b
```

Configure in `openclaw.json`:

```json
"agents": {
  "defaults": {
    "memorySearch": {
      "enabled": true,
      "provider": "ollama",
      "model": "qwen3-embedding:8b"
    }
  }
}
```

OpenClaw's Ollama embedding provider automatically reads the base URL from `models.providers.ollama.baseUrl` (already configured as `http://127.0.0.1:11434`).

### Verify

```bash
openclaw memory status --deep
openclaw memory index --force
```

You should see `Embeddings: ready` and `Vector: ready` for each agent.

## Quick Reference: Key Config Paths

| Config Path | Purpose |
|---|---|
| `channels.feishu.groupPolicy` | Feishu group message policy (`open` / `allowlist`) |
| `agents.defaults.contextPruning` | Auto-trim old tool outputs |
| `agents.defaults.compaction` | Auto-compress history when context is full |
| `agents.defaults.memorySearch` | Semantic search over past conversations |
| `agents.list[].tools` | Per-agent tool restrictions (`deny`, `profile`, `exec`) |
| `workspace/TOOLS.md` | Agent behavior rules (read every session) |

## Lessons Learned

- `openclaw doctor --fix` catches and fixes a lot of common misconfigurations automatically
- Context pruning is the single most impactful setting for keeping sessions healthy
- Subagent delegation is better than tool restrictions for handling large outputs — isolation beats limitation
- Ollama as a local embedding provider works well if you have the RAM (qwen3-embedding:8b needs ~5GB)
- Cron jobs need explicit `delivery.to` — the error message is clear but easy to miss
