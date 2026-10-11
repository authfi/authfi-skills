---
type: Howto
title: "Accept agents at your own API"
description: "Verify an AI agent's access token in your service, read who is calling, and check the action a transaction token is bound to."
tags: [authfi, ai-agent, jwt, eddsa, audience, verification]
sources:
  - id: agents-verify
    resource: https://authfi.io/docs/agents/verify
    title: "Accept agents at your own API"
---

# Accept agents at your own API

Your service verifies the token itself, without calling AuthFI. Use a JWT library that supports `EdDSA`.

## Give the agent a token for your API

1. Register your API as an application under **Integrations > Applications**. Its client ID is how a token names your API.
2. Grant the agent access to that application.
3. The agent requests a token with `resource` set to the API's client ID.

An agent with no grant on your API gets `invalid_target`.

## Verify the access token

| Check | Expect |
| --- | --- |
| Signature | Verifies with the key named by `kid`, from the project's `/.well-known/jwks.json` |
| `alg` | `EdDSA` |
| `typ` | `at+jwt` |
| `iss` | The project's issuer |
| `aud` | Your API's client ID |
| `exp` | In the future |

```js
import { createRemoteJWKSet, jwtVerify } from "jose";

const keys = createRemoteJWKSet(new URL("https://acme.authfi.io/.well-known/jwks.json"));

export async function verifyAgent(token) {
  const { payload } = await jwtVerify(token, keys, {
    issuer: "https://acme.authfi.io",
    audience: process.env.API_CLIENT_ID,
    algorithms: ["EdDSA"],
    typ: "at+jwt",
  });
  return payload;
}
```

## Read who is calling

| Claim | Tells you |
| --- | --- |
| `client_id` | The agent, always. `agt_…` |
| `sub` | The agent, or the person it is acting for |
| `act.sub` | Present when the agent acts for a person: the agent, as `agent:agt_…` |
| `agent_type` | `delegated` or `autonomous` |
| `capabilities` | The names of what the agent was granted |

Decide what the caller may do from `capabilities`, and record `client_id` with everything it does.

## Check a transaction token

For a sensitive action, require a transaction token as well as the access token. Check the signature, `iss`, `aud` and `exp` as above, `typ` is `txn_token+jwt`, and `sub` is the same agent. Then compare `azd.action`, `azd.resource` and `azd.context` with the request in front of you. Reject the request if anything differs.

## When an agent is revoked

A service that checks only the signature accepts the token until it expires, at most 15 minutes later. To reject it sooner, receive revocation events. See [revocation.md](revocation.md).

## Detail

Python sample, the remaining claims and troubleshooting: [Accept agents at your own API](https://authfi.io/docs/agents/verify)
