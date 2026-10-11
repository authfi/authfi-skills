---
type: Howto
title: "Protect a web app with Zero-Code"
description: "Put the project's sign-in in front of a service people open in a browser, and read who is signed in from request headers."
tags: [authfi, zero-code, sign-in, session, headers, web-app]
sources:
  - id: zero-code-protect-ui
    resource: https://authfi.io/docs/zero-code/protect-ui
    title: "Protect a web app"
---

# Protect a web app with Zero-Code

A person who opens the service is sent to the project's sign-in page and brought back with a session, with no change to the service's code.

## Steps in the console

1. Open **Zero-Code > Kubernetes**, select the cluster, and on the **Workloads** tab choose **Classify** on the workload's row.
2. Choose **App**, turn on **Pages** under **What does it serve?**, and choose **Continue to Protect**.
3. Turn on **Pages · require sign-in**. Enter the **Hostname** people use, and choose how long the **Signed-in session lasts**: 1 hour, 8 hours or 24 hours.
4. Under **What it may reach**, tick the destinations the service needs.
5. Choose **Save draft**. Saving registers an application for this hostname.
6. Point the hostname's DNS at your cluster's ingress.
7. On the **Pages** card, follow **Choose who may use it** and **Assign a group**.
8. When the audit record reads right, choose **Turn on protection…** and confirm.

Until the application is assigned to a group, anyone who can sign in to the project can open it.

## Read who is signed in

Every request that reaches the service carries who is making it. The service needs no token library.

| Header | Value |
| --- | --- |
| `X-AuthFI-User-ID` | The person |
| `X-AuthFI-User-Email` | Their email |
| `X-AuthFI-Groups` | Their groups, separated by commas |
| `X-AuthFI-Roles` | Their roles, separated by commas |
| `X-AuthFI-Permissions` | Their permissions, separated by commas |
| `X-AuthFI-Session-ID` | The session, for your logs |

```python
@app.get("/reports")
def reports(request):
    email = request.headers["X-AuthFI-User-Email"]
    groups = request.headers.get("X-AuthFI-Groups", "").split(",")
    if "finance" not in groups:
        return Response(status=403)
    return render_reports(for_user=email)
```

Any header beginning `X-AuthFI-` that a caller sends is removed before the request reaches the service. What you read was set by the node, never by the caller.

When an AI agent calls instead of a person, the request also carries `X-AuthFI-Agent-ID` and `X-AuthFI-Agent-Capabilities`, and `X-AuthFI-On-Behalf-Of` when the agent acts for someone.

## The session

| Setting | Value |
| --- | --- |
| Session cookie | `authfi_session`, for this hostname only, `Secure` and `HttpOnly` |
| Sign-out | Send the browser to `/__authfi/logout` on the service's hostname |

A session is for one service. It is not accepted at another.

## Check that it works

In a browser with no session, open a page on the service. The browser is sent to the project's sign-in page, and after sign-in returns to the page you asked for.

## Detail

[Protect a web app](https://authfi.io/docs/zero-code/protect-ui)
