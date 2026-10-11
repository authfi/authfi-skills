---
type: Reference
title: "Error shapes and codes"
description: "How AuthFI reports a failure on each surface, what the common codes mean and what to do about each."
tags: [authfi, errors, oauth, troubleshooting, status-codes]
sources:
  - id: reference-errors
    resource: https://authfi.io/docs/reference/errors
    title: "Errors"
  - id: reference-oauth
    resource: https://authfi.io/docs/reference/oauth
    title: "OAuth and OpenID Connect endpoints"
---

# Error shapes and codes

Find the surface you called, then the code.

## Response shapes

| Surface | Shape |
| --- | --- |
| OAuth endpoints and the agent token endpoint | OAuth 2.0 (RFC 6749): `error`, and sometimes `error_description` |
| The authorization endpoint | The same fields, with `state`, in the query string of the redirect URI |
| Other endpoints | A code in `error`, with the matching HTTP status. A success puts its result under `data`. |
| Zero-Code | `403` with `error`, `message` and `ref` |
| MCP gateway | A JSON-RPC error, or a tool result with `isError` set |

## OAuth endpoints for applications

| `error` | Status | What to do |
| --- | --- | --- |
| `invalid_request` | `400` | Send every required parameter. Register the exact redirect URI, with path and port. |
| `invalid_client` | `401` | Check the client ID, the issuer and the client secret |
| `invalid_grant` | `400` | Start a new sign-in. Exchange each code once, within 5 minutes. |
| `unauthorized_client` | `400` | Use an `m2m` application for `client_credentials` |
| `unsupported_grant_type` | `400` | Use `authorization_code`, `refresh_token` or `client_credentials` |
| `invalid_scope` | `400` | Ask for a subset of the scopes first granted |
| `invalid_target` | `400` | Name the API's client ID, and grant the caller access to that API |
| `access_denied` | `403` | Assign the application to the person or one of their groups |
| `login_required` | `401` | Send the person to sign in again |
| `interaction_required` | `401` | Send the person to the sign-in page |
| `unmet_authentication_requirements` | `400` | Enrol the person in MFA or a passkey, or ask for a lower value |
| `insufficient_user_authentication` | `401` | Send the person to sign in with the `acr_values` required |
| `temporarily_unavailable` | `503` | Try again shortly |
| `rate_limited` | `429` | Wait, then send fewer requests |

A refresh token that was already used returns `invalid_grant` and revokes every token from the same sign-in.

## Agent token endpoint

| `error` | What to do |
| --- | --- |
| `invalid_request` | Send the body form-encoded, with every required field |
| `invalid_client` | Check `kid`, `aud`, the clock, and that `jti` is new |
| `unsupported_grant_type` | Use `client_credentials` |
| `invalid_target` | Ask an administrator to grant the agent access to that target |
| `temporarily_unavailable` | Try again shortly |

While polling with the CIBA grant, each with status `400`: `authorization_pending` (wait `interval` seconds), `slow_down` (wait longer), `access_denied` (stop) and `expired_token` (stop, or ask again).

## Other endpoints

| Status | `error` | Meaning |
| --- | --- | --- |
| `400` | `invalid_body` | The request body is missing a field or is not valid JSON |
| `401` | `unauthorized` | No credential, or one that is expired or revoked |
| `403` | | The caller is known and is not allowed to do this |
| `404` | | Nothing with that identifier exists in this project |
| `429` | | More than 300 requests a minute from one IP address |

## Zero-Code denials

| Denied as | What to do |
| --- | --- |
| `missing_token` | Send an access token as `Authorization: Bearer` |
| `invalid_token` | Get a new access token |
| `not_an_access_token` | Send the access token, not the ID token |
| `audience_mismatch` | Ask for a token with `resource` set to this API's client ID |
| `policy_denied` | Give the caller what the rule requires, or change the rule |

The `ref` in the response identifies the denial in the audit record.

## MCP gateway

`401` means no token, or one that is expired or revoked. JSON-RPC codes are `-32700` (not valid JSON), `-32601` (unknown method), `-32602` (wrong parameters) and `-32000` (tool server unreachable). A denied call is a tool result with `isError` set, beginning `Denied by policy` or `Approval required`.

## Detail

The meaning of every code, and agent decisions: [Errors](https://authfi.io/docs/reference/errors)
