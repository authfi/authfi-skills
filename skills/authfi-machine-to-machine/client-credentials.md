---
type: Howto
title: "Get a token with the client credentials grant"
description: "Register a machine-to-machine application, grant it an API, and request an access token for that API."
tags: [authfi, client-credentials, m2m, resource, audience]
sources:
  - id: applications-machine-to-machine
    resource: https://authfi.io/docs/applications/machine-to-machine
    title: "Get an access token for a backend service"
---

# Get a token with the client credentials grant

## Set up in the console

1. Open **Integrations > Applications** and choose **Register**.
2. Select **OIDC / OAuth 2.0**, then the kind **Machine-to-machine**, and enter a **Name**.
3. The **Done** step shows the client ID and the **Client secret**, once. Copy both.
4. On the application's page, choose **Allow an API** and allow the API you want to call. The APIs it can call are listed under **APIs it may call**.

## Request the token

The body is form-encoded. The client ID and secret go in HTTP Basic authentication.

```bash
curl https://acme.authfi.io/oauth/token \
  -u "$CLIENT_ID:$CLIENT_SECRET" \
  -d grant_type=client_credentials \
  -d resource="$API_CLIENT_ID"
```

| Parameter | Value |
| --- | --- |
| `grant_type` | `client_credentials` |
| `resource` | The client ID of the one API the token is for |
| `scope` | Optional. The scopes to put in the token. |

```json
{ "access_token": "eyJ...", "token_type": "Bearer", "expires_in": 900 }
```

`expires_in` is in seconds. When the access token expires, request another.

## What the token contains

| Claim | Value |
| --- | --- |
| `sub` | The calling service's client ID |
| `client_id` | The calling service's client ID |
| `aud` | The API named in `resource` |
| `scope` | The scopes you asked for, unchanged |
| `exp` | 15 minutes after issue, unless the project changed it |

The token has no `sid`, `amr` or `acr` claim, because no person signed in.

## Check that it works

Decode the payload of the access token. The flow works when `sub` and `client_id` are the calling service's client ID, and `aud` contains the API's client ID.

## Detail

Node.js and Python samples, and the full procedure: [Get an access token for a backend service](https://authfi.io/docs/applications/machine-to-machine)
