Title: Building an OpenClaw Plugin: Five Pitfalls I Hit So You Don't Have To
Date: 2026-04-02
Slug: building-an-openclaw-plugin-task-monitor
Category: Coding
Tags: OpenClaw, Plugin, LLM, Agent, Subagent, TypeScript
Summary: I built a plugin that adds step-level task tracking and auto-retry to OpenClaw subagent runs. The plugin system is well-designed, but five gotchas cost me hours of debugging.

I wanted my OpenClaw main agent to track subagent progress at the step level, persist state to disk, and auto-retry on failure — none of which the built-in `sessions_spawn` provides. So I built `task-monitor` as a native OpenClaw plugin. The plugin system is powerful, but the gap between documentation and runtime behavior is real. Here are the five pitfalls I hit.

## What the Plugin Does

Four tools, two hooks:

| Tool | Who | Purpose |
|------|-----|---------|
| `task_spawn` | main agent | Create task + delegate to subagent, write initial state |
| `task_status` | main agent | Read progress from state file |
| `task_retry` | main agent | Resume failed task from last completed step |
| `task_checkpoint` | subagent | Update step status after completing each step |

Two hooks: `subagent_ended` (auto-retry on failure) and `before_prompt_build` (inject task context into subagent prompt).

State lives in `~/.openclaw/task-monitor/state/<taskId>.json` — shared between gateway process and subagent processes via the filesystem.

## Pitfall 1: `@sinclair/typebox` Must Be Installed Locally

Plugin code runs inside the OpenClaw gateway process via jiti, but module resolution doesn't share the host's `node_modules`. You need a local `package.json` with dependencies:

```bash
cd ~/Projects/Claws/task-monitor
npm install @sinclair/typebox
```

Without this, `openclaw plugins inspect` shows `Cannot find module '@sinclair/typebox'` and the plugin fails to load.

## Pitfall 2: `tools.profile` Eats Plugin Tools

This was the most insidious bug. My config had:

```json
"tools": {
  "profile": "coding",
  "allow": ["task_spawn", "task_checkpoint", "task_status", "task_retry"]
}
```

The agent kept saying "I don't have `task_spawn`." The plugin loaded fine, `openclaw plugins inspect` showed all four tools — but the agent couldn't see them.

The root cause: `coding` profile enables a `stripPluginOnlyAllowlist` pipeline step. When `tools.allow` contains **only plugin tool names** (no core tools), the entire allow list gets silently discarded. The logic treats plugin-only allowlists as "probably a mistake" and drops them.

The fix is `tools.alsoAllow` instead of `tools.allow`:

```json
"tools": {
  "profile": "coding",
  "alsoAllow": ["task_spawn", "task_checkpoint", "task_status", "task_retry"]
}
```

`alsoAllow` merges into `profileAlsoAllow`, which bypasses the strip logic. From the source code (`tool-policy-ZLsNmkQQ.js`):

```javascript
// if every entry is a plugin tool, hasCoreEntry stays false
// and the entire allow list gets voided:
const strippedAllowlist = !hasCoreEntry;
if (strippedAllowlist) {
  policy = { ...policy, allow: void 0 }
}
```

The distinction: `allow` = whitelist intersection (profile-filtered), `alsoAllow` = additive on top of profile.

## Pitfall 3: `SubagentRunParams.idempotencyKey` Is Actually Required

The TypeScript types say it's optional:

```typescript
export type SubagentRunParams = {
  sessionKey: string;
  message: string;
  idempotencyKey?: string;  // "optional"
};
```

But the runtime validator throws: `must have required property 'idempotencyKey'`. A types-vs-runtime mismatch in OpenClaw itself. You must always pass it:

```typescript
await runtime.subagent.run({
  sessionKey,
  message,
  deliver: false,
  idempotencyKey: `task-monitor:${taskId}`,  // required
});
```

## Pitfall 4: `registerHook` Needs a `name` Option

Without it, you get `WARN: hook registration missing name` on every startup:

```typescript
// noisy
api.registerHook("subagent_ended", handler);

// clean
api.registerHook("subagent_ended", handler, {
  name: "task-monitor:auto-retry",
});
```

## Pitfall 5: `openclaw plugins inspect` Lulls You Into False Confidence

`plugins inspect` queries the plugin registry — it shows registered tools, hooks, and status. But the agent's tool list is computed by a separate policy pipeline. A tool can be registered in the plugin system and completely invisible to the agent.

Don't trust `inspect` as proof that tools work. Test by actually sending a message to the agent and checking if it can call the tool.

## Verification Checklist

```bash
# plugin loads
openclaw plugins inspect task-monitor

# no errors in log
grep "task_spawn\|task.*fail" ~/.openclaw/logs/gateway.err.log

# agent can actually use the tool (send via feishu)
# agent should NOT say "I don't have this tool"

# state files get created
ls ~/.openclaw/task-monitor/state/
```

## File Structure

```
~/Projects/Claws/task-monitor/
  package.json
  openclaw.plugin.json
  index.ts
  src/
    types/state.ts, config.ts
    state-manager.ts
    tools/task-spawn.ts, task-checkpoint.ts, task-status.ts, task-retry.ts
    hooks/subagent-ended.ts, before-prompt-build.ts
    config.ts, store.ts
```

Symlinked into `~/.openclaw/plugins/task-monitor`, loaded via `plugins.load.paths` in `openclaw.json`.
