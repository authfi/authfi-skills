---
type: Reference
title: "Application types and redirect URIs"
description: "Which AuthFI application type to register, whether it holds a client secret, and how a redirect URI is matched."
tags: [authfi, application, redirect-uri, client-secret, pkce]
sources:
  - id: applications-types
    resource: https://authfi.io/docs/applications/types
    title: "Application types and redirect URIs"
---

# Application types and redirect URIs

## The four types

The type follows from where the code runs. Code on a server can keep a secret. Code in a browser or on a device cannot.

| Type | Kind in the console | For | Client secret | Signs in with |
| --- | --- | --- | --- | --- |
| `web` | Web application | A web app with a server | Yes | Authorization code, with its client secret |
| `spa` | Single-page app | An application that runs in the browser | No | Authorization code with PKCE |
| `native` | Android app, iOS or macOS app | A mobile or desktop application | No | Authorization code with PKCE |
| `m2m` | Machine-to-machine | A backend service calling another service | Yes | Client credentials |

Only an `m2m` application can use `client_credentials`. Any other type is rejected with `unauthorized_client`.

## Client ID and client secret

- AuthFI generates the client ID. You do not choose it.
- The client secret is shown once, on the last step of registration.
- If it is lost, rotate it on the application's page: **Credential** section, **Rotate the secret**. The old secret stops working at once.
- Send the secret to the token endpoint as HTTP Basic authentication or as `client_secret` in the body.

## How a redirect URI is matched

The `redirect_uri` you send must be exactly one of the registered URIs.

| Registered | Accepted |
| --- | --- |
| `http://127.0.0.1` | `http://127.0.0.1:53124/callback`, on any port |
| `http://localhost` | `http://localhost:3000/callback`, on any port |
| `https://app.acme.com/callback` | That URI only |

When it does not match, AuthFI answers with a `400` page on the project's issuer. The browser is never sent to a URI that is not registered.

To change redirect URIs later, open the **Credential** section of the application's page and choose **Edit registration**.

## Who can sign in

An application is open to everyone in the project until you assign it to a group with **Assign a group**. From the first assignment, only members of the assigned groups can sign in. Assignment is checked when the person is sent to sign in, and again each time a token is issued.

## Detail

[Application types and redirect URIs](https://authfi.io/docs/applications/types)
