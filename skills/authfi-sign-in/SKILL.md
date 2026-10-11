---
name: authfi-sign-in
type: Skill
title: "Sign people in with AuthFI"
description: "Use when adding sign-in to a web app, single-page app or native app with AuthFI over OpenID Connect, or when handling redirect URIs, refresh tokens, sign-out or MFA for signed-in people."
tags: [authfi, oidc, oauth, pkce, sign-in, sessions, mfa]
sources:
  - id: quickstart-sign-in
    resource: https://authfi.io/docs/quickstart/sign-in
    title: "Add sign-in to an app"
  - id: applications-types
    resource: https://authfi.io/docs/applications/types
    title: "Application types and redirect URIs"
  - id: applications-sessions
    resource: https://authfi.io/docs/applications/sessions
    title: "Manage sessions, sign-out and MFA"
  - id: reference-oauth
    resource: https://authfi.io/docs/reference/oauth
    title: "OAuth and OpenID Connect endpoints"
---

# Sign people in with AuthFI

AuthFI signs a person in with the OpenID Connect authorization code flow and PKCE (RFC 7636). Any OpenID Connect library works: give it the issuer and the client ID, and it reads the rest from `/.well-known/openid-configuration`.

## What you need from the developer

- The project's issuer, for example `https://acme.authfi.io`.
- The application's client ID, from **Integrations > Applications** in the AuthFI console. A web application also has a client secret, shown once at registration.
- The redirect URI registered for the application.

## Rules that apply every time

1. **Use the authorization code flow.** `response_type=code` is the only value.
2. **Send PKCE with `S256`.** It is required for an application with no client secret and accepted from one with a secret. `plain` is rejected.
3. **`redirect_uri` must match a registered URI exactly**: scheme, host, port, path and query. No wildcards. The one exception is a loopback URI registered with no port, which accepts any port.
4. **Compare `state` on return.** If it differs from the value you stored, stop.
5. **Exchange each code once, within 5 minutes.**
6. **Validate the ID token** with issuer = the project's issuer, audience = your client ID, algorithm `RS256`, keys from `jwks_uri`.
7. **The ID token is not a bearer credential.** Call APIs with the access token.
8. **Keep the client secret on a server.** A browser or native app has no secret and sends `client_id` only.
9. **Use each refresh token once and store the new one.** Presenting a used refresh token revokes every token from that sign-in.
10. **Check `acr` and `auth_time` yourself** before a sensitive action. Asking for a level is not the same as getting it.

## Pitfalls

| What you see | Cause |
| --- | --- |
| A `400` page with `invalid_request` instead of the sign-in page | The `redirect_uri` is not registered exactly |
| A `401` page with `invalid_client` | The client ID is not an application in this project |
| The browser returns with `error=access_denied` | The application is assigned to groups, and the person is in none |
| `invalid_grant` at the token endpoint | The code expired, was used already, or the verifier does not match |
| `invalid_client` at the token endpoint | The client secret is missing or wrong |

## Files in this skill

| File | Read it when |
| --- | --- |
| [authorization-code-flow.md](authorization-code-flow.md) | You are wiring the flow, by library or by hand |
| [application-types.md](application-types.md) | You are choosing a type or fixing a redirect URI |
| [sessions-and-mfa.md](sessions-and-mfa.md) | You need refresh, sign-out, a fresh sign-in or MFA |

For claims and error codes, load `authfi-tokens-and-errors`.
