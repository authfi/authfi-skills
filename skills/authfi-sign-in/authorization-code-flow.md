---
type: Howto
title: "Run the authorization code flow with PKCE"
description: "The requests an application makes to sign a person in with AuthFI, and the values a library needs."
tags: [authfi, oidc, pkce, authorization-code, id-token]
sources:
  - id: quickstart-sign-in
    resource: https://authfi.io/docs/quickstart/sign-in
    title: "Add sign-in to an app"
  - id: reference-oauth
    resource: https://authfi.io/docs/reference/oauth
    title: "OAuth and OpenID Connect endpoints"
---

# Run the authorization code flow with PKCE

## With a library

Configure an OpenID Connect library with these values. It does the rest.

| Setting | Value |
| --- | --- |
| Issuer | `https://acme.authfi.io` |
| Client ID | From the console |
| Client secret | Web application only |
| Redirect URI | A registered URI, exactly |
| Scope | `openid profile email` |
| PKCE method | `S256` |

## Register the application

In the console, open **Integrations > Applications** and select **Register**. Choose **OIDC / OAuth 2.0**, then **Web application** (runs on a server, keeps a secret) or **Single-page app** (runs in the browser, uses PKCE). Enter a **Name** and the **Redirect URIs**, one per line. The last step shows the **Client id**, and for a web application the **Client secret**, once.

## The flow on the wire

1. **Create a verifier, a challenge and a `state`.** The challenge is the base64url SHA-256 hash of the verifier. Keep the verifier and `state` in the person's session on your server.
2. **Redirect the browser** to `GET /oauth/authorize` with `response_type=code`, `client_id`, `redirect_uri`, `scope`, `state`, `code_challenge` and `code_challenge_method=S256`.
3. **Receive the code.** The browser returns to your redirect URI with `code`, `state` and `iss`. Compare `state`.
4. **Exchange the code** at `POST /oauth/token`. The body is form-encoded.

```bash
curl https://acme.authfi.io/oauth/token \
  -d grant_type=authorization_code \
  -d code="$CODE" \
  -d redirect_uri=https://app.acme.com/callback \
  -d client_id="$CLIENT_ID" \
  -d code_verifier="$VERIFIER"
```

A web application also sends its client secret, as HTTP Basic authentication or as `client_secret` in the body.

5. **Validate the ID token**, then read who signed in from it.

## What comes back

| Token | Use it to | Lifetime |
| --- | --- | --- |
| `id_token` | Learn who signed in | 15 minutes by default |
| `access_token` | Call APIs on the person's behalf | 15 minutes by default |
| `refresh_token` | Get new tokens without another sign-in | 30 days by default |

The ID token carries `sub`, `email`, `email_verified`, `name`, `groups` and `roles` whatever scopes you request. Scopes decide what `GET /oauth/userinfo` returns: `email` adds the email fields, `profile` adds `name`, `picture`, `locale`, `groups` and `roles`.

## Check that it works

```bash
curl https://acme.authfi.io/oauth/userinfo \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

If the response names the person you signed in as, the flow works end to end.

## Detail

- Step by step, with Shell, Node.js and Python samples: [Add sign-in to an app](https://authfi.io/docs/quickstart/sign-in)
- Every parameter, including `nonce`, `prompt`, `max_age`, `acr_values` and `login_hint`: [OAuth and OpenID Connect endpoints](https://authfi.io/docs/reference/oauth)
