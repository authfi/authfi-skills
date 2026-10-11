---
name: authfi-mcp-gateway
type: Skill
title: "Call tools through the AuthFI MCP gateway"
description: "Use when connecting an MCP tool server to an AuthFI project, granting tools to an AI agent, calling tools through the project's MCP gateway, or handling a denied call or one that needs approval."
tags: [authfi, mcp, ai-agent, tools, json-rpc, approvals]
sources:
  - id: quickstart-mcp
    resource: https://authfi.io/docs/quickstart/mcp
    title: "Connect an agent to tools"
  - id: agents-mcp-gateway
    resource: https://authfi.io/docs/agents/mcp-gateway
    title: "The MCP gateway"
---

# Call tools through the AuthFI MCP gateway

Each project has a gateway for the Model Context Protocol (MCP) at `/mcp` on its issuer, for example `https://acme.authfi.io/mcp`. Agents connect to it instead of to each tool server. The gateway checks every call against what the agent was granted, holds the tool server's credential so the agent never sees it, makes a call wait for a person when a rule says so, and records each call.

## What you need from the developer

- The project's issuer.
- A registered agent and an access token whose `resource` is the gateway. Load `authfi-agent-auth` to get one.
- The tool server's URL, and the bearer token it expects if it needs one.

## Rules that apply every time

1. **Point the agent at the gateway URL, not at the tool server.**
2. **Send the agent's access token as a Bearer credential.** An agent token requested with no `resource` is issued for the gateway.
3. **Nothing is callable until it is granted.** A grant is on one tool. Granting one tool on a server does not grant the others.
4. **Tool names are `namespace.tool`.** The namespace you choose when you connect a server prefixes every tool on it.
5. **The gateway answers three methods**: `initialize`, `tools/list` and `tools/call`, as JSON-RPC 2.0 over HTTP `POST`, MCP revision `2025-06-18`.
6. **A denial is a tool result, not an HTTP error.** It is an ordinary tool result with `isError` set, so the model reads it and can change course.
7. **On "Approval required", repeat the same call with `_authfi_approval_id`** once a person has approved. An approval is good for 15 minutes and for that call.
8. **On `401`, sign the agent in again.** The token is missing, expired or revoked.

## Files in this skill

| File | Read it when |
| --- | --- |
| [connect-and-call.md](connect-and-call.md) | You are connecting a tool server, granting a tool or making a call |
| [denials-and-approvals.md](denials-and-approvals.md) | A call was denied, needs approval or returned an error |
