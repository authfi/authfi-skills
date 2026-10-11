---
name: authfi-zero-code
type: Skill
title: "Protect Kubernetes services with AuthFI Zero-Code"
description: "Use when putting AuthFI sign-in or access-token checks in front of a service on Kubernetes without changing its code, installing Zero-Code on a cluster, writing route rules, or reading the identity headers a protected service receives."
tags: [authfi, zero-code, kubernetes, helm, route-rules, headers]
sources:
  - id: zero-code-overview
    resource: https://authfi.io/docs/zero-code/overview
    title: "How Zero-Code works"
  - id: zero-code-enforcement
    resource: https://authfi.io/docs/zero-code/enforcement
    title: "How enforcement works"
  - id: zero-code-install
    resource: https://authfi.io/docs/zero-code/install
    title: "Install Zero-Code on a cluster"
  - id: zero-code-protect-ui
    resource: https://authfi.io/docs/zero-code/protect-ui
    title: "Protect a web app"
  - id: zero-code-protect-api
    resource: https://authfi.io/docs/zero-code/protect-api
    title: "Protect an API"
---

# Protect Kubernetes services with AuthFI Zero-Code

Zero-Code puts sign-in and access rules in front of services that run on Kubernetes. It does on the node what a sign-in library would do inside the application. You install it once on a cluster: an operator, and a _node agent_ that runs on every node. Nothing is added to your pods, and your services are not rebuilt or restarted.

On Zero-Code pages, "node agent" is the component on a cluster node. "AI agent" is a registered agent identity.

## What it decides

| Capability | What you get |
| --- | --- |
| Sign-in | A person opening a service in a browser is sent to the project's sign-in page and brought back with a session |
| Token checks | A program calling an API must present a valid access token issued for that API |
| Route rules | Which roles and groups may call each route |
| Connection rules | Where each workload and each AI agent may connect |

## The three steps

Every workload goes through **Observe**, **Classify** and **Protect** in the console, under **Zero-Code > Kubernetes**, on the cluster's **Workloads** tab.

## Rules that apply every time

1. **A protected service needs no sign-in or token library.** It reads the caller from the `X-AuthFI-` request headers.
2. **Everything starts in monitor mode.** Nothing is denied until you turn protection on. A saved draft records what it would deny.
3. **A workload is watched for 24 hours before it can be protected.** Until then **Turn on protection…** is unavailable. Save the draft and read the audit record in the meantime.
4. **An API with rules is closed by default.** Once protected, a request that matches no rule is denied, including callers that work today.
5. **A token is for one API.** A caller names the API's audience in `resource`. A token issued for another API is denied with `audience_mismatch`.
6. **Send the access token, not the ID token.** An ID token is denied with `not_an_access_token`.
7. **Some paths are always let through** without a token, such as `/health` and `/.well-known/*`. Do not serve anything private under them.
8. **A pages application is open until first assigned.** Assign it to a group to close it to everyone else.
9. **Rules reach the nodes in about 30 seconds.** A connection already open is left alone until it closes.
10. **Change install settings through Helm values.** Do not edit the `AgentRuntime` object.

## Files in this skill

| File | Read it when |
| --- | --- |
| [install.md](install.md) | You are connecting, checking, upgrading or removing a cluster |
| [protect-web-app.md](protect-web-app.md) | People open the service in a browser |
| [protect-api.md](protect-api.md) | Programs call the service with a token |
| [enforcement.md](enforcement.md) | You need to know what is denied, where, and how to stop it |
