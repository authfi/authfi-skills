---
type: Howto
title: "Revoke an agent and receive revocation events"
description: "What revoking an AI agent stops, and how your own service is told the moment it happens."
tags: [authfi, ai-agent, revocation, shared-signals, ssf]
sources:
  - id: agents-revocation
    resource: https://authfi.io/docs/agents/revocation
    title: "Revoke an agent"
---

# Revoke an agent and receive revocation events

## Revoke

An administrator revokes an agent on its page under **Identity > AI Agents**, from "More actions".

| Action | Use it when |
| --- | --- |
| **Revoke credential** | The agent must stop |
| **Revoke as compromised** | You believe the agent's key was stolen |

**Revocation cannot be undone.** A revoked agent stays revoked. If you need the agent again, register a new one.

## What revocation stops

| Where | What happens |
| --- | --- |
| Sign-in | A request for a new token gets `invalid_client` |
| The MCP gateway | The agent's next call is denied, even with an unexpired token |
| Approvals and authorize | Denied |
| Nodes running Zero-Code | Reject the agent's remaining tokens |
| Any other service | Sees the token as inactive if it asks AuthFI |

A service that checks only the signature accepts the agent's access token until it expires, at most 15 minutes later.

## Receive revocation events

AuthFI pushes a signed event to your server, using OpenID Shared Signals.

1. Read `https://acme.authfi.io/.well-known/ssf-configuration`. `configuration_endpoint` is where a receiver is registered.
2. An administrator registers the receiver there.

| Field | Meaning |
| --- | --- |
| `audience` | A value you choose. It is the `aud` of every event sent to you. |
| `endpoint_url` | Where to send events. It must be `https`. |
| `auth_token` | Optional. Sent back to you as a Bearer credential. |
| `events_requested` | Optional. The event types you want. |

3. Events arrive by HTTP `POST` (RFC 8935). Each is a signed token. Before you act on one:
   - Verify the signature against the project's keys, at `jwks_uri`.
   - Check that `iss` is your project's issuer.
   - Check that `aud` is the audience you registered.
4. Then stop accepting that agent's tokens.

## Revoke or delete

Deleting permanently removes the agent and its record of what it was allowed to do. Revoke first, and delete only when you no longer need that record.

## Detail

[Revoke an agent](https://authfi.io/docs/agents/revocation)
