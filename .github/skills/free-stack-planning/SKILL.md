---
name: free-stack-planning
description: 'Plan a zero-budget or free-tier architecture for research, demos, documentation, and lightweight APIs. Use for deciding when no server is needed, when to add a server, and which free hosting option fits the project.'
argument-hint: '[product idea, MVP, or workflow]'
---

# Free Stack Planning

## When To Use

- You need an execution plan that stays at zero cost as long as possible.
- You want to know whether a server is necessary or avoidable.
- You need a phase-by-phase hosting and compute strategy for a prototype.

## Procedure

1. Default to local-first and no-server architecture.
2. Add a hosted component only when there is a concrete need: shared docs, shareable demo, public API, or background jobs.
3. Match each need to the cheapest acceptable layer.
4. Document the quota, sleep behavior, privacy limits, and vendor lock-in risk.
5. Separate what is viable now from what only becomes necessary after validation.

## Recommended Decision Order

1. No server
2. Static hosting
3. Demo app hosting
4. Serverless API
5. Shared storage or background jobs

## Output Shape

- Default architecture
- Trigger for adding a server
- Free options by layer
- Limits and quotas
- Recommended phased rollout

## Guardrails

- Avoid paid orchestration, vector databases, and observability stacks until the MVP is proven.
- Prefer open exchange formats and local exports before proprietary integrations.
