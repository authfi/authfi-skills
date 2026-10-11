---
type: Howto
title: "Validate a token and handle key rotation"
description: "The checks a service makes on an AuthFI token, the library settings for each token type, and what to do when a signing key rotates."
tags: [authfi, jwt, validation, jwks, key-rotation, audience]
sources:
  - id: reference-tokens
    resource: https://authfi.io/docs/reference/tokens
    title: "Tokens and claims"
  - id: security-keys
    resource: https://authfi.io/docs/security/keys
    title: "Keys and secrets"
  - id: reference-oauth
    resource: https://authfi.io/docs/reference/oauth
    title: "OAuth and OpenID Connect endpoints"
---

# Validate a token and handle key rotation

## The checks

Most JWT libraries make these checks when you configure them with the issuer, the keys URL, the audience and the algorithm.

1. Verify the signature with the key whose `kid` matches the token's header.
2. Check that `iss` is the issuer of the project you trust.
3. Check that `aud` names this service. Reject a token issued for another service.
4. Check that `exp` is in the future.
5. For a bearer token, check that the header `typ` is `at+jwt`.

## Library settings

| Setting | ID token | Access token | Agent access token |
| --- | --- | --- | --- |
| Issuer | The project's issuer | The project's issuer | The project's issuer |
| Keys | `/.well-known/jwks.json` | `/.well-known/jwks.json` | `/.well-known/jwks.json` |
| Audience | Your client ID | The client ID it was issued to. For a service's token, your API's client ID. | Your API's client ID |
| Algorithm | `RS256` | `RS256` | `EdDSA` |
| `typ` | `JWT` | `at+jwt` | `at+jwt` |

For a transaction token, also compare `azd` with the request in front of you, and reject any difference.

Before a sensitive action, read `acr` from the token and deny the action if it is weaker than you need.

## Key rotation

A project's administrator rotates a signing key on their own schedule.

| Time | What happens |
| --- | --- |
| At once | A new key signs every new token |
| For 24 hours | The old key stays published, so tokens it signed still verify |
| After 24 hours | The old key is removed |

A service keeps working through a rotation when it follows three rules.

- **Find the key by `kid`.** Never pin one key, and never assume the first key in the set.
- **Fetch the key set again when you meet a `kid` you do not know**, then cache it. Do not fetch on every request.
- **Cache for hours, not days.** If a token names a key you cannot find, fetch once more before you reject the token.

Disabling a key is different: it removes the key from the published set at once, and every token it signed stops verifying.

## Ask AuthFI instead

An application with a client secret can ask whether an access token is active.

```bash
curl https://acme.authfi.io/oauth/token/introspect \
  -u "$CLIENT_ID:$CLIENT_SECRET" \
  -d token="$ACCESS_TOKEN"
```

A token that is expired, malformed or not an access token returns `{"active": false}` and no other field.

## Detail

- [Checking a token](https://authfi.io/docs/reference/tokens#checking-a-token)
- [Keys and secrets](https://authfi.io/docs/security/keys)
