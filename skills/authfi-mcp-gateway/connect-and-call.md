---
type: Howto
title: "Connect a tool server and call a tool"
description: "Connect an MCP tool server to the gateway, grant a tool to an agent, and list and call tools with the agent's access token."
tags: [authfi, mcp, tools, grant, tools-list, tools-call]
sources:
  - id: quickstart-mcp
    resource: https://authfi.io/docs/quickstart/mcp
    title: "Connect an agent to tools"
  - id: agents-mcp-gateway
    resource: https://authfi.io/docs/agents/mcp-gateway
    title: "The MCP gateway"
  - id: reference-discovery
    resource: https://authfi.io/docs/reference/discovery
    title: "Discovery documents"
---

# Connect a tool server and call a tool

## Connect the tool server

In the console, open **Integrations > MCP Gateway**, select the **Servers** tab, and select **Connect a server**.

| Field | Enter |
| --- | --- |
| **Namespace** | One short name: letters, digits and dashes. It prefixes every tool's name. |
| **Server URL** | Where the tool server is reached |
| **Transport** | The transport the tool server uses |
| **How it authenticates the gateway** | **Bearer token** or **No credential** |
| **Whose credential** | **One shared credential** or **Each user's own** |
| **Credential** | The token the tool server expects |

Select **Register**. The gateway reads the server's tools and lists each one as `namespace.tool` on the **Tools** tab.

## Grant a tool

On the **Tools** tab, select **Say who may call a tool**. Choose the kind of caller (an AI agent, a person or a group), choose the caller, tick the tools, and select the **Grant** button. A grant to a group reaches every member of it.

## Find the gateway URL

On the **Overview** tab, under **Where the agents connect**, **Gateway** is the URL the agent calls. It is also `resource` in `/.well-known/oauth-protected-resource`.

## List the tools

```bash
curl https://acme.authfi.io/mcp \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

`tools/list` returns every tool, each marked with what would happen if this agent called it.

| `io.authfi/governance` | Meaning |
| --- | --- |
| `no_policy_restriction` | This agent may call it |
| `may_require_approval` | A person may have to approve, depending on the arguments |
| `never_allowed` | This agent's call is denied |

The decision itself is made on each call, with its arguments.

## Call a tool

```bash
curl https://acme.authfi.io/mcp \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": { "name": "tickets.reply", "arguments": { "ticket": "4821", "text": "On it." } }
  }'
```

The gateway checks the call, forwards it to the tool server with the tool's own credential, and returns the tool's result.

## Check that it works

In the console, open the **Tape** tab of **Integrations > MCP Gateway**. The row for your call shows the caller, the tool and a **Verdict** of **allowed**.

## Per-person credentials

With **Each user's own**, each person connects their own account with **Connect my account** on the **Servers** tab. The gateway then makes each call with the account of the person the agent is acting for. A call with no person, or for a person who has not connected their account, is denied.

## Detail

- First call, step by step: [Connect an agent to tools](https://authfi.io/docs/quickstart/mcp)
- Every check, credentials and what is recorded: [The MCP gateway](https://authfi.io/docs/agents/mcp-gateway)
