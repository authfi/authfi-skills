---
type: Reference
title: "Denied calls, approvals and gateway errors"
description: "What the MCP gateway checks on a call, and how a denial, an approval request and each error are reported."
tags: [authfi, mcp, errors, approvals, json-rpc, denial]
sources:
  - id: agents-mcp-gateway
    resource: https://authfi.io/docs/agents/mcp-gateway
    title: "The MCP gateway"
  - id: reference-errors
    resource: https://authfi.io/docs/reference/errors
    title: "Errors"
---

# Denied calls, approvals and gateway errors

## What is checked on a call

For every `tools/call`, in order:

1. The token is a valid agent access token for this project.
2. The agent has not been revoked.
3. The agent is granted this tool.
4. If the agent is acting for a person, that person is granted it too.
5. The arguments pass the project's rules.

## Three levels of failure

| Level | Looks like | Means |
| --- | --- | --- |
| HTTP | `401` with a `WWW-Authenticate` header | No token, or one that is expired or revoked |
| JSON-RPC | An `error` with a code | The gateway could not process the request |
| Tool result | A `result` with `isError` set | The gateway denied the call, or it needs approval |

## The `401`

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer resource_metadata="https://acme.authfi.io/.well-known/oauth-protected-resource"
```

The document at that URL names the gateway and the project as its authorization server (RFC 9728). Sign the agent in again and send the new token.

## JSON-RPC errors

| Code | Meaning | What to do |
| --- | --- | --- |
| `-32700` | The body is not valid JSON | Send valid JSON |
| `-32601` | The method is not `initialize`, `tools/list` or `tools/call` | Use one of the three methods |
| `-32602` | The parameters are wrong | Correct `params` and send the request again |
| `-32000` | The tool server could not be reached | Check the server's URL in the console, then retry |

## A denied call

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "result": {
    "isError": true,
    "content": [{ "type": "text", "text": "Denied by policy: agent:agt_7f3a9c21 is not granted payments.refund" }]
  }
}
```

| Result text begins | Meaning | What to do |
| --- | --- | --- |
| `Denied by policy` | The gateway denied the call. The text gives the reason. | Grant the tool, or change the arguments |
| `Approval required` | A rule sends the call to a person | After approval, repeat the call with `_authfi_approval_id` |

## A call that needs approval

The result text carries an approval ID. A person approves or denies the request on the **Approvals** page of the console. The agent then makes the same call again and adds the approval ID to the arguments:

```json
{
  "jsonrpc": "2.0",
  "id": 8,
  "method": "tools/call",
  "params": {
    "name": "payments.refund",
    "arguments": { "payment": "pay_4821", "amount": 1200, "_authfi_approval_id": "3f0c2b6e-…" }
  }
}
```

The gateway checks the approval, removes `_authfi_approval_id`, and forwards the call. The tool server never sees the approval ID. An approval is good for 15 minutes and for that call.

## Detail

[The MCP gateway](https://authfi.io/docs/agents/mcp-gateway) and the MCP section of [Errors](https://authfi.io/docs/reference/errors)
