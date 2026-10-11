---
type: Howto
title: "Refresh tokens, sign-out and MFA"
description: "Keep a person signed in, sign them out, and require a fresh sign-in or multi-factor authentication from an application."
tags: [authfi, sessions, refresh-token, sign-out, mfa, acr]
sources:
  - id: applications-sessions
    resource: https://authfi.io/docs/applications/sessions
    title: "Manage sessions, sign-out and MFA"
  - id: reference-oauth
    resource: https://authfi.io/docs/reference/oauth
    title: "OAuth and OpenID Connect endpoints"
---

# Refresh tokens, sign-out and MFA

## Keep a person signed in

```bash
curl https://acme.authfi.io/oauth/token \
  -d grant_type=refresh_token \
  -d refresh_token="$REFRESH_TOKEN" \
  -d client_id="$CLIENT_ID"
```

- **Use each refresh token once.** Every use returns a new one. Store it and discard the old one.
- **Ask for the same scopes, or fewer.** More returns `invalid_scope`.
- **`sid`, `amr` and `auth_time` do not change on refresh.** Refreshing does not make a sign-in look newer.
- **A reused refresh token signs the person out.** AuthFI revokes every token from the same sign-in and answers `invalid_grant`.

An application with a client secret always receives a refresh token. An application without one receives it when the project allows it, which is the default.

## Sign a person out

Send the browser to the end-session endpoint.

```text
https://acme.authfi.io/oauth/logout?client_id=CLIENT_ID&post_logout_redirect_uri=https%3A%2F%2Fapp.acme.com%2F&state=abc
```

The person is sent back only when `client_id` is given and `post_logout_redirect_uri` has the scheme and host of a registered redirect URI. Otherwise they see a signed-out page.

Signing out ends the session. To also stop the refresh token your application holds, revoke it at `POST /oauth/token/revoke` with `token` and `client_id`. The response is `200` with an empty body.

An access token stays valid until it expires. Revocation acts on refresh tokens.

## Require a fresh sign-in

Add one of these to the authorization request.

| Parameter | Effect |
| --- | --- |
| `prompt=login` | The person signs in again, even with a session |
| `max_age=600` | The person signs in again if they last did so more than 600 seconds ago |
| `login_hint` | Fills in the account name on the sign-in page |

When you depend on `max_age`, check `auth_time` in the ID token yourself.

## Require MFA

Add `acr_values` to the authorization request.

| `acr_values` | The person must have |
| --- | --- |
| `urn:authfi:acr:1fa` | Signed in |
| `urn:authfi:acr:mfa` | Completed MFA |
| `urn:authfi:acr:passkey` | Signed in with a passkey |
| `urn:authfi:acr:passkey_mfa` | Used a passkey and completed MFA |

Several values, separated by spaces, mean "any of these, or stronger". If the level cannot be reached, the browser returns with `error=unmet_authentication_requirements`. Read `acr` from the token before a sensitive action and deny if it is weaker than you need.

## Default lifetimes

| Item | Default |
| --- | --- |
| Access token and ID token | 15 minutes |
| Refresh token | 30 days |
| Session, total length | 24 hours |
| Session, idle time | 8 hours |

An administrator changes these in **Settings > Sessions** in the console.

## Detail

Console steps, the `amr` values and the sign-in protections every project applies are in [Manage sessions, sign-out and MFA](https://authfi.io/docs/applications/sessions).
