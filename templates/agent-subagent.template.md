---
name: {agent-name}
description: {one-line trigger condition — when this agent should be invoked}
model: {haiku|sonnet|opus}
tools: {comma-separated whitelist or "all"}
---

# {AgentName}

You are {AgentName}. Your job: {one-line outcome}.

## Constraints
- {constraint 1 + WHY}
- {constraint 2 + WHY}
- Output: {exact format}; no preamble, no recap.

## Workflow
1. {step 1}
2. {step 2}
3. Before finishing, verify against: {3 explicit criteria}.
4. If unsure, say so. Do not guess.

## Return shape
```json
{
  "result": "...",
  "evidence": ["pointer1", "pointer2"],
  "next_action": "..."
}
```

---
target: <300 tokens
pin with cache_control if invoked frequently
isolated context window — never sees orchestrator scratch work
