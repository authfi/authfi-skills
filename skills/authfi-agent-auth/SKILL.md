---
name: authfi-agent-auth
type: Skill
title: "AI agent identity with AuthFI"
description: "Use when giving an AI agent its own AuthFI identity, signing it in with its key, limiting what it may do, asking a person to approve an action, accepting agent tokens at an API, or revoking an agent."
tags: [authfi, ai-agent, private-key-jwt, ciba, approvals, capabilities]
sources:
  - id: quickstart-agent
    resource: https://authfi.io/docs/quickstart/agent
    title: "Give an AI agent an identity"
  - id: agents-how-it-works
    resource: https://authfi.io/docs/agents/how-it-works
    title: "How agent sign-in works"
  - id: agents-limits
    resource: https://authfi.io/docs/agents/limits
    title: "Limit what an agent may do"
  - id: agents-approvals
    resource: https://authfi.io/docs/agents/approvals
    title: "Ask before a sensitive action"
  - id: agents-mcp-gateway
    resource: https://authfi.io/docs/agents/mcp-gateway
    title: "The MCP gateway"
  - id: reference-errors
    resource: https://authfi.io/docs/reference/errors
    title: "Errors"
---

# AI agent identity with AuthFI

An AI agent in AuthFI is an identity of its own, with its own key, its own permissions and a named owner. It signs in with `private_key_jwt` (RFC 7523) and an Ed25519 key, and receives an access token that lasts 15 minutes. AuthFI combines published OAuth standards, so any client that speaks OAuth 2.0 can act as an agent.

## What you need from the developer

- The project's issuer.
- The agent ID, which starts with `agt_`. It is the agent's `client_id`, shown on the agent's **Connect** tab under **Identity > AI Agents**.
- The key ID registered for the agent, and the private key, which stays with the agent.

## Rules that apply every time

1. **An agent holds a key, never a shared secret.** Register the public half only. The private key never leaves the agent.
2. **Build a new client assertion for every request.** An assertion is accepted once and expires within 5 minutes. Use a new `jti` each time. Sending one again returns `invalid_client`.
3. **The assertion's `aud` is the token endpoint's full URL.** Read `token_endpoint` from `/.well-known/oauth-authorization-server`.
4. **Sign with `EdDSA`** and put the registered key ID in the `kid` header.
5. **Name the target in `resource`.** It becomes the token's `aud`. An agent can name only the targets it was granted. Any other gets `invalid_target`. With no `resource`, the token is issued for the project's MCP gateway.
6. **There is no refresh token.** When the access token expires, sign a new assertion and request another.
7. **An agent starts with no permissions.** Everything not granted is denied. The console says _permission_ where the docs say _capability_.
8. **Tokens carry capability names, never their limits.** AuthFI checks limits each time the agent acts, so a changed limit applies to the next call.
9. **`approval_required` is not a failure.** The action waits for a person. An unanswered request expires, and expired means denied.
10. **A service must check `aud`.** Accept an agent token only when `aud` names that service.

## Two types of agent

| Type | Acts as | Answers to |
| --- | --- | --- |
| `delegated` | A named person | That person, its owner |
| `autonomous` | Itself | A group, its approval group |

The type is set at registration and appears in every token as `agent_type`.

## Files in this skill

| File | Read it when |
| --- | --- |
| [agent-sign-in.md](agent-sign-in.md) | You are registering an agent or getting its first token |
| [limits-and-decisions.md](limits-and-decisions.md) | You are granting capabilities, writing limits or reading a decision |
| [approvals.md](approvals.md) | The agent must ask before acting, or ask a named person |
| [verify-agent-tokens.md](verify-agent-tokens.md) | Your own API must accept agent tokens |
| [revocation.md](revocation.md) | An agent must be stopped, or your service must hear about it |

For tool calls, load `authfi-mcp-gateway`. For every claim and error code, load `authfi-tokens-and-errors`.
