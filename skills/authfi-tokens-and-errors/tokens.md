---
type: Reference
title: "Token types and claims"
description: "Each token an AuthFI project issues, what signs it, how long it lasts and the claims it carries."
tags: [authfi, tokens, claims, id-token, access-token, acr]
sources:
  - id: reference-tokens
    resource: https://authfi.io/docs/reference/tokens
    title: "Tokens and claims"
---

# Token types and claims

## Token types

| Token | Issued to | Signed with | Header `typ` | Lifetime |
| --- | --- | --- | --- | --- |
| ID token | An application, after a person signs in | `RS256` | `JWT` | 15 minutes by default |
| Access token | An application or a service | `RS256` | `at+jwt` | 15 minutes by default |
| Refresh token | An application, after a person signs in | Not a JWT | | 30 days by default, used once |
| Agent access token | An AI agent, after it signs in | `EdDSA` | `at+jwt` | 15 minutes by default |
| Transaction token | An agent, for one action | `EdDSA` | `txn_token+jwt` | 60 seconds |
| Client assertion | Made by the agent itself, to sign in | The agent's own key | `JWT` | At most 5 minutes, used once |

## ID token

Tells an application who signed in. `aud` is the client ID it was issued to.

| Claim | Description |
| --- | --- |
| `sub` | The person's identifier in this project |
| `auth_time` | When the person last signed in |
| `nonce` | The `nonce` your application sent, unchanged |
| `email`, `email_verified`, `name` | The person's email and name |
| `groups` | The groups assigned to the application, or shared with it, that the person is in |
| `roles` | The roles the person holds |

## Access token

Lets an application or a service call an API. It follows the JWT access token profile (RFC 9068).

| Claim | Description |
| --- | --- |
| `sub` | The person, or for a service its own client ID |
| `aud` | A list. For a person, the client ID it was issued to. For a service, the API named in `resource`. |
| `client_id` | The application the token was issued to |
| `scope` | The scopes granted, space-separated |
| `roles`, `permissions`, `groups` | What the person holds |
| `sid` | The session the token came from |
| `amr`, `acr` | How the person signed in |
| `jti` | A unique identifier for this token |

A service's token has no `sid`, `amr` or `acr`, because nobody signed in.

## Agent access token

| Claim | Description |
| --- | --- |
| `sub` | The agent, or the person it is acting for |
| `client_id` | The agent ID, `agt_…`. Always the agent. |
| `aud` | Where the token may be used, from `resource` in the request |
| `agent_type` | `delegated` or `autonomous` |
| `act` | Present when the agent acts for a person. `act.sub` is the agent, as `agent:agt_…`. |
| `capabilities` | The names of the capabilities the agent was granted |
| `scope` | The same grants, as a space-separated string |

## Sign-in strength

| `acr` | The person |
| --- | --- |
| `urn:authfi:acr:1fa` | Signed in |
| `urn:authfi:acr:mfa` | Completed multi-factor authentication (MFA) |
| `urn:authfi:acr:passkey` | Signed in with a passkey |
| `urn:authfi:acr:passkey_mfa` | Signed in with a passkey and completed MFA |

`amr` is the list of methods the person used, such as `pwd`, `otp`, `mfa`, `hwk`, `user` and `fed`.

## Custom claims

A claim that a webhook action returns is added to the token under `custom`.

## Detail

Every claim of every token, including the transaction token: [Tokens and claims](https://authfi.io/docs/reference/tokens)
