---
type: Concept
title: "Projects, issuers and discovery"
description: "How a client finds every AuthFI endpoint and signing key from the project's issuer alone."
tags: [authfi, issuer, discovery, jwks, well-known]
sources:
  - id: concepts-projects
    resource: https://authfi.io/docs/concepts/projects
    title: "Projects and issuers"
  - id: reference-discovery
    resource: https://authfi.io/docs/reference/discovery
    title: "Discovery documents"
---

# Projects, issuers and discovery

## One project, one issuer

A project has one URL of the form `https://<project>.authfi.io`. That URL is the issuer. It is the `iss` claim of every token the project signs, and the only value a client is configured with. The region a project runs in is never part of the issuer.

## Discovery documents

Each document is at a fixed path on the issuer and needs no authentication.

| Document | Describes | Standard |
| --- | --- | --- |
| `/.well-known/openid-configuration` | Sign-in for people and applications | OpenID Connect Discovery |
| `/.well-known/oauth-authorization-server` | The token endpoint for AI agents | RFC 8414 |
| `/.well-known/agent-configuration` | Agent endpoints and approval methods | AuthFI |
| `/.well-known/oauth-protected-resource` | The MCP gateway as a protected resource | RFC 9728 |
| `/.well-known/jwks.json` | The project's public signing keys | RFC 7517 |
| `/.well-known/ssf-configuration` | Revocation events you can subscribe to | OpenID Shared Signals |

```bash
curl https://acme.authfi.io/.well-known/openid-configuration
```

Read these fields instead of typing URLs:

- People and applications: `authorization_endpoint`, `token_endpoint`, `userinfo_endpoint`, `end_session_endpoint`, `revocation_endpoint`, `introspection_endpoint`, `jwks_uri` from `openid-configuration`.
- AI agents: `token_endpoint` and `backchannel_authentication_endpoint` from `oauth-authorization-server`.
- MCP: `resource` from `oauth-protected-resource` is the gateway URL.

A project also publishes SAML 2.0 metadata at `/saml/metadata`.

## Signing keys

The key set holds one `RS256` key and one `EdDSA` (Ed25519) key.

| Key | Signs |
| --- | --- |
| `RS256` | ID tokens and access tokens for people and services |
| `EdDSA` | Tokens for AI agents |

Match a token's `kid` header to a key in the set. Keys rotate, and a rotated key stays published for 24 hours. Cache the set, and fetch it again when you meet a `kid` you do not have.

## Detail

The full contents of every document, with an example response and each field, are in [Discovery documents](https://authfi.io/docs/reference/discovery).
