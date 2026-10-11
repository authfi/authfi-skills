---
type: Reference
title: "Capabilities, limits, rules and decisions"
description: "How an AI agent's capabilities, limits and project rules combine into an allow, deny or approval decision."
tags: [authfi, ai-agent, capabilities, limits, policy, decision]
sources:
  - id: agents-limits
    resource: https://authfi.io/docs/agents/limits
    title: "Limit what an agent may do"
  - id: reference-errors
    resource: https://authfi.io/docs/reference/errors
    title: "Errors"
---

# Capabilities, limits, rules and decisions

## Three things decide

- A **capability** is a named permission, such as `payments.transfer`. An agent can do only what it has been granted. Grant one on the agent's **Permissions** tab with **Grant a permission**.
- A **limit** is a condition on the details of one action. It belongs to one capability on one agent.
- A **rule** applies to every agent and every person in the project. It can deny an action, or make it wait for a person. The console calls a rule a _policy_.

## Limit forms

Limits are JSON. Each key names a field of the `context` the agent sends when it asks before acting.

```json
{
  "amount": { "max": 5000 },
  "currency": { "in": ["USD", "EUR"] },
  "region": { "not_in": ["sanctioned"] },
  "account_type": "business"
}
```

| Form | Passes when |
| --- | --- |
| `{ "max": 5000 }` | The value is a number, 5000 or less |
| `{ "min": 1 }` | The value is a number, 1 or more |
| `{ "in": [...] }` | The value is one of the list |
| `{ "not_in": [...] }` | The value is not in the list |
| A plain value | The value is exactly that |

**A field named in `max`, `min` or `in` must be sent.** A request that leaves it out is denied. Always send every limited field in `context`.

## The decision and its reason

| `decision` | `reason` | Meaning |
| --- | --- | --- |
| `allow` | `resource_grant`, `relationship` | Something granted it |
| `deny` | `no_match` | Nothing granted it |
| `deny` | `policy_deny` | A rule denies it |
| `deny` | `constraint_violated: …` | A limit on the capability was exceeded |
| `approval_required` | `policy_step_up` | A rule sends it to a person |

A decision is a successful response, not an error. The same reason is written to the audit record.

## The order of a decision

1. Is the agent known and not revoked? If not, the response is `401`.
2. Do the action's details pass the limits on the capability? If not, `deny`.
3. Does a rule deny it? If so, `deny`. No grant overrides a deny.
4. Is it granted? If not, `deny`.
5. Does a rule ask for a person? If so, `approval_required`.
6. Otherwise, `allow`.

## Delegated agents

A delegated agent that acts for a person through the MCP gateway can do only what both of them may do. The agent's grants and the person's grants are both checked.

## Detail

Console steps for granting a capability, writing a project rule and testing a decision under **Security > Authorization**: [Limit what an agent may do](https://authfi.io/docs/agents/limits)
