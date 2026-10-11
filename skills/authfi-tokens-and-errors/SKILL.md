---
name: authfi-tokens-and-errors
type: Skill
title: "AuthFI tokens, claims and errors"
description: "Use when validating an AuthFI token in a service, reading a claim, handling signing-key rotation, or working out what an AuthFI error code means and what to do about it."
tags: [authfi, jwt, claims, jwks, errors, validation]
sources:
  - id: reference-tokens
    resource: https://authfi.io/docs/reference/tokens
    title: "Tokens and claims"
  - id: reference-errors
    resource: https://authfi.io/docs/reference/errors
    title: "Errors"
  - id: security-keys
    resource: https://authfi.io/docs/security/keys
    title: "Keys and secrets"
---

# AuthFI tokens, claims and errors

A project issues several kinds of token. Each is signed with one of the project's keys, published at `/.well-known/jwks.json` on the issuer. A service validates a JWT itself, without a call to AuthFI.

## Rules that apply every time

1. **Make all five checks**: signature by `kid`, `iss` is the project you trust, `aud` names this service, `exp` is in the future, and for a bearer token the header `typ` is `at+jwt`.
2. **Pass the algorithm explicitly.** `RS256` for tokens issued to people and services, `EdDSA` for tokens issued to AI agents.
3. **Reject a token issued for another service.** `aud` must name yours.
4. **Never accept an ID token as a bearer credential.** It has `typ: JWT`.
5. **Find the key by `kid`.** Never pin one key, and never assume the first key in the set.
6. **Fetch the key set again on an unknown `kid`**, then cache it. Do not fetch on every request. Cache for hours, not days.
7. **An access token carries no name or email.** Read those from the ID token or from userinfo.
8. **`groups` is not every group.** It lists the groups assigned to the application or shared with it.
9. **A signature check accepts a token until it expires.** To learn sooner, subscribe to revocation events or call the introspection endpoint.
10. **Find the surface before the code.** An error's shape depends on what you called: OAuth endpoints, other endpoints, Zero-Code or the MCP gateway.

## Lifetimes

| Token | Lifetime |
| --- | --- |
| ID token and access token | 15 minutes by default |
| Refresh token | 30 days by default, used once |
| Agent access token | 15 minutes by default |
| Transaction token | 60 seconds |
| Client assertion | At most 5 minutes, used once |

## Files in this skill

| File | Read it when |
| --- | --- |
| [tokens.md](tokens.md) | You need to know what a token is for or what a claim means |
| [validating-tokens.md](validating-tokens.md) | You are writing or reviewing token validation, or handling key rotation |
| [errors.md](errors.md) | You have an error code or a denial and need the cause and the fix |
