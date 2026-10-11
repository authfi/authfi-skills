---
type: Howto
title: "Register an agent and sign it in"
description: "Register an AI agent with its public key, build a client assertion, and get a 15-minute access token."
tags: [authfi, ai-agent, private-key-jwt, ed25519, client-assertion]
sources:
  - id: quickstart-agent
    resource: https://authfi.io/docs/quickstart/agent
    title: "Give an AI agent an identity"
  - id: agents-how-it-works
    resource: https://authfi.io/docs/agents/how-it-works
    title: "How agent sign-in works"
  - id: reference-discovery
    resource: https://authfi.io/docs/reference/discovery
    title: "Discovery documents"
---

# Register an agent and sign it in

## Register the agent

1. Generate an Ed25519 key pair where the agent runs. Keep the private key with the agent, and nowhere else.
2. In the console, open **Identity > AI Agents** and select **Register agent**. The steps are **Name it**, **Its key**, **What it may do**, **Who it acts for**, **Review** and **Done**.
3. On **Its key**, select **The agent already has one**, paste the public JWK and enter a **Key id**, for example `agent-key-1`.
4. On **What it may do**, allow the permissions the agent needs.
5. The **Done** step shows the **Agent id**, which starts with `agt_`.

The public JWK has this shape. Paste the public half only.

```json
{ "kty": "OKP", "crv": "Ed25519", "x": "11qYAYKxCrfVS_7TyWQHOg7hcvPapiMlrwIaaPcHURo" }
```

The console can also make the key: **Make the key here** generates the pair in the browser, and the **Done** step shows the private key once.

## Find the token endpoint

```bash
curl https://acme.authfi.io/.well-known/oauth-authorization-server
```

Use `token_endpoint` from the response. The agent token endpoint is separate from the one applications use.

## Build the client assertion

A JWT signed with the agent's private key.

| Part | Value |
| --- | --- |
| Header `alg` | `EdDSA` |
| Header `kid` | The key ID you registered |
| `iss` and `sub` | The agent ID |
| `aud` | The token endpoint's full URL |
| `jti` | A new random value every time |
| `exp` | At most 5 minutes after `iat` |

## Request the token

`POST` to the token endpoint, form-encoded, with these fields.

| Field | Value |
| --- | --- |
| `grant_type` | `client_credentials` |
| `client_id` | The agent ID |
| `client_assertion_type` | `urn:ietf:params:oauth:client-assertion-type:jwt-bearer` |
| `client_assertion` | The signed assertion |
| `resource` | Where the token will be used, for example `https://acme.authfi.io/mcp` |

```json
{
  "access_token": "eyJhbGciOiJFZERTQSIs…",
  "token_type": "Bearer",
  "expires_in": 900,
  "agent_id": "agt_7f3a9c21",
  "type": "autonomous",
  "capabilities": ["tickets.read", "tickets.reply"]
}
```

Send `access_token` as a Bearer credential in the `Authorization` header.

## Check that it works

Decode the access token's payload. `iss` is your issuer, `client_id` is the agent ID, and `agent_type` is `autonomous` or `delegated`.

## Troubleshooting

| `error` | Cause | Fix |
| --- | --- | --- |
| `invalid_client` | The agent ID is unknown, the agent was revoked, or the assertion did not verify | Check `kid`, `aud` and the clock, and that `jti` is new |
| `invalid_target` | `resource` names something this agent has not been granted | Ask an administrator to grant the agent that target |
| `unsupported_grant_type` | `grant_type` is missing or not one this endpoint offers | Use `client_credentials` |
| `invalid_request` | The body could not be read | Send the body form-encoded |

## Detail

Complete key-generation and sign-in scripts in Node.js and Python: [Give an AI agent an identity](https://authfi.io/docs/quickstart/agent)
