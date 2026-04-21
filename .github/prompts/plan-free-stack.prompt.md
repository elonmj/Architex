---
description: 'Build a zero-budget execution plan with local-first defaults and free-tier hosting only when needed.'
name: plan-free-stack
argument-hint: '[MVP, workflow, or product slice]'
agent: agent
---

Plan a free execution stack for: ${input:scope:current workspace project}

Requirements:

- Assume zero budget by default.
- Start with no server and justify any hosted component.
- Distinguish documentation hosting, demo hosting, API hosting, storage, and compute.
- Include quotas, sleep behavior, privacy constraints, and migration triggers.
- End with a phased plan and the minimum stack to start this week.
