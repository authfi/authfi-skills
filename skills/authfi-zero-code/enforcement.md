---
type: Concept
title: "Monitor mode, enforce mode and the brake"
description: "When a Zero-Code rule denies, what a denied caller sees, and how the cluster owner stops all denials."
tags: [authfi, zero-code, enforcement, monitor-mode, brake]
sources:
  - id: zero-code-enforcement
    resource: https://authfi.io/docs/zero-code/enforcement
    title: "How enforcement works"
  - id: zero-code-overview
    resource: https://authfi.io/docs/zero-code/overview
    title: "How Zero-Code works"
  - id: reference-errors
    resource: https://authfi.io/docs/reference/errors
    title: "Errors"
---

# Monitor mode, enforce mode and the brake

## Two modes

In _monitor mode_, a rule denies nothing and records what it would have denied. In _enforce mode_, the rule is applied. Everything starts in monitor mode.

| Level | Set by | Meaning |
| --- | --- | --- |
| The cluster | `mode` in the install | `observe`: the nodes are in monitor mode. `enforce`: the nodes may deny. |
| A workload | **Turn on protection…** in the console | Monitor mode until you turn protection on, then enforce mode |

A protected workload's rules apply on the nodes running it whatever the node mode.

## What a caller sees

| Caller | Answer |
| --- | --- |
| A browser with no session | A redirect to the sign-in page |
| A person not assigned to the application | A `403` page that says so |
| A token for another API | `403`, wrong audience |
| A workload connecting where it was not granted | The connection fails with `EPERM` |
| Any caller, when the node agent has no rules yet | `503` with `Retry-After` |

Every denial is written to the audit record with the layer that denied it.

## Connection rules

For each workload you list where it may connect: the destinations, and the ports on them. In enforce mode, every other destination is denied. Outbound access is closed by default. If a protected workload cannot reach a dependency, add the destination and port under **What it may reach**.

A workload classified as **AI agent** is held more tightly. It cannot reach the cloud metadata address `169.254.169.254`, and no grant opens it. It calls tools through the MCP gateway.

## The brake

The cluster owner holds a switch that AuthFI cannot override. It is a field on the install's `AgentRuntime` resource.

```yaml
spec:
  enforcementInhibit: true
```

With the brake on, the nodes stop denying. Everything is still monitored and recorded. Take the brake off, and the rules in force resume.

## Timing

- Rules reach a node within 30 seconds of a change.
- A connection already open when a workload is switched to enforce mode is left alone until it closes. To have existing connections checked at once, restart the workload.
- If the project cannot be reached, a node keeps enforcing the last rules it received.

## Detail

[How enforcement works](https://authfi.io/docs/zero-code/enforcement)
