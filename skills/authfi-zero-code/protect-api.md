---
type: Howto
title: "Protect an API with Zero-Code"
description: "Require an access token issued for one API, write route rules for who may call each route, and read each denial."
tags: [authfi, zero-code, api, audience, route-rules, access-token]
sources:
  - id: zero-code-protect-api
    resource: https://authfi.io/docs/zero-code/protect-api
    title: "Protect an API"
---

# Protect an API with Zero-Code

Zero-Code checks every call on the node, before the request reaches your code. The service does not verify tokens, fetch keys or parse claims.

## Steps in the console

1. Open **Zero-Code > Kubernetes**, select the cluster, and on the **Workloads** tab choose **Classify** on the workload's row.
2. Choose **App**, turn on **API** under **What does it serve?**, and choose **Continue to Protect**.
3. Turn on **API · software calls it**.
4. Under **Route rules**, choose **Fill in the draft** to load rules drafted from observed traffic, then correct them.
5. Under **What it may reach**, tick the destinations the service needs.
6. Choose **Save draft**. Saving registers the API as an application. On the **API** card, **Copy audience**.
7. Grant each caller access: **Grant an application access to it** on the **API** card, or **Allow an API** on a machine-to-machine application's page.
8. When the audit record reads right, choose **Turn on protection…** and confirm.

A caller asks for a token by naming the audience in `resource`. A service uses client credentials (`authfi-machine-to-machine`). An AI agent uses agent sign-in (`authfi-agent-auth`).

## What is checked on each request

| Check | Denied as |
| --- | --- |
| There is a `Bearer` token | `missing_token` |
| It is signed by your project, and has not expired | `invalid_token` |
| The AI agent or session behind it has not been revoked | `invalid_token` |
| It is an access token, not an ID token | `not_an_access_token` |
| It was issued for this API | `audience_mismatch` |
| The route's rule is met | `policy_denied` |

A denied request receives `403` with `error`, `message` and `ref`. `ref` identifies the denial in the audit record. Give it to whoever asks why they were denied.

## Route rules

- A rule names a method and a path: an exact path, or a prefix ending in `/*`. A path starts with `/`.
- Each rule is **Signed in** or **Anyone**, plus requirements chosen from the project's roles, groups and permissions.
- A caller needs every permission listed and any one of the groups or roles.
- More specific rules are tried first: an exact path before a prefix, and a longer prefix before a shorter one. The first rule that matches decides.
- Once the workload is protected, a request that matches no rule is denied.

## Paths that are always let through

| Kind | Paths |
| --- | --- |
| Health | `/health`, `/healthz`, `/livez`, `/ready`, `/readyz` |
| Discovery | `/.well-known/*` |
| Sign-in | `/login`, `/register`, `/signup`, `/callback`, `/oauth/callback`, `/auth/*` equivalents, and `POST` to `/token` |
| Browser basics | `/favicon.ico`, `/robots.txt`, `/static/*`, `/assets/*`, any `OPTIONS` request |

These paths are public. A request to one of them reaches the service without a token.

## Read who is calling

The request reaches the service with `X-AuthFI-User-ID`, `X-AuthFI-Groups` and `X-AuthFI-Roles`. A request from an AI agent also carries `X-AuthFI-Agent-ID`.

## Hand a service back

On the cluster's **Services** tab, choose **Unprotect** on the service's row and confirm with **Hand it back**.

## Detail

The route rule controls, an example rule set and troubleshooting: [Protect an API](https://authfi.io/docs/zero-code/protect-api)
