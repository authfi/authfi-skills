---
name: authfi-machine-to-machine
type: Skill
title: "Service-to-service tokens with AuthFI"
description: "Use when a backend service with no signed-in person needs an AuthFI access token to call another API, using the OAuth client credentials grant."
tags: [authfi, oauth, client-credentials, m2m, service-to-service]
sources:
  - id: applications-machine-to-machine
    resource: https://authfi.io/docs/applications/machine-to-machine
    title: "Get an access token for a backend service"
  - id: reference-oauth
    resource: https://authfi.io/docs/reference/oauth
    title: "OAuth and OpenID Connect endpoints"
---

# Service-to-service tokens with AuthFI

A backend service signs in as itself with the `client_credentials` grant (RFC 6749, section 4.4) and receives an access token for the one API it calls.

This is for a service that holds a client secret. An AI agent holds its own key and never a shared secret: load `authfi-agent-auth` for that.

## What you need from the developer

- The project's issuer.
- The calling service's client ID and client secret, from a **Machine-to-machine** application.
- The client ID of the API it calls. The API is registered as an application in the same project.

## Rules that apply every time

1. **Only a machine-to-machine application may use this grant.** Any other type gets `unauthorized_client`.
2. **`resource` is required, and it is the API's client ID.** It becomes the token's `aud`.
3. **Grant the caller access to the API first.** Without a grant on the API's application, the request gets `invalid_target`.
4. **One token, one API.** To call two APIs, request two tokens, one for each `resource`.
5. **There is no refresh token and no ID token.** When the access token expires, request another. It lasts 15 minutes unless the project changed it.
6. **The API checks `aud`.** It validates the token against the project's keys and checks that `aud` contains its own client ID.
7. **The client secret is shown once.** If it is lost, choose **Rotate the secret** on the application's page.

## Pitfalls

| What you see | Cause | Fix |
| --- | --- | --- |
| `invalid_client` | The client ID is unknown, or the client secret is wrong | Check both values |
| `unauthorized_client` | The application is not of the kind **Machine-to-machine** | Register the caller as **Machine-to-machine** |
| `invalid_target` | `resource` is not an application, or the service has no grant on it | Send the API's client ID, and use **Allow an API** on the caller's page |

## Files in this skill

| File | Read it when |
| --- | --- |
| [client-credentials.md](client-credentials.md) | You are registering the caller or writing the token request |

For validating the token at the API, load `authfi-tokens-and-errors`.
