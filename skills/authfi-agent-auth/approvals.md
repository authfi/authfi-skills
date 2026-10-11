---
type: Howto
title: "Ask before a sensitive action"
description: "Bind a transaction token to one action, ask AuthFI for a decision, and wait for a person or a named person to approve."
tags: [authfi, ai-agent, approvals, transaction-token, ciba, human-in-the-loop]
sources:
  - id: agents-approvals
    resource: https://authfi.io/docs/agents/approvals
    title: "Ask before a sensitive action"
  - id: agents-ciba
    resource: https://authfi.io/docs/agents/ciba
    title: "Ask a named person to approve"
---

# Ask before a sensitive action

There are two ways to put a person in the loop. Pick by who must answer.

| Who answers | Use | The agent receives |
| --- | --- | --- |
| The agent's owner or approval group | Transaction token, then authorize | A decision, and an approval to poll |
| One named person | CIBA, in poll mode | An access token that names that person |

## Owner or approval group

All paths below are on the project's issuer.

| Step | Request | Sends | Returns |
| --- | --- | --- | --- |
| 1. Bind a token to the action | `POST /apis/regional/v1/ai/auth/transaction-token`, with the access token as Bearer | `action`, `resource`, `context` | `transaction_token`, valid 60 seconds |
| 2. Ask for the decision | `POST /apis/regional/v1/agents/authorize` | `agent_id`, `transaction_token`, and the same `action`, `resource`, `context` | `decision`, and `approval_id` when a person is needed |
| 3. Wait for a person | `GET /apis/regional/v1/agents/approvals/{approval_id}` | | `status` |

Bodies are JSON, and results are under `data`.

```json
{ "data": { "decision": "approval_required", "approval_id": "3f0c2b6e-…" } }
```

- The action, resource and context are frozen inside the transaction token. Send exactly the same values in step 2.
- On `allow`, go ahead. On `deny`, stop and read `reason`. On `approval_required`, poll with `approval_id`.

| Approval `status` | What the agent does |
| --- | --- |
| `pending` | Keeps polling |
| `approved` | Goes ahead |
| `denied` | Stops |
| `expired` | Stops |

The person answers on the **Approvals** page of the console. An agent cannot approve through its own credentials.

## One named person, with CIBA

1. `POST` to `backchannel_authentication_endpoint` from `/.well-known/oauth-authorization-server`, form-encoded, with `client_id`, a fresh client assertion, and:

| Parameter | Meaning |
| --- | --- |
| `login_hint` | Required. The person to ask, by the name they sign in with. |
| `scope` | What the agent wants to do with this person's authority |
| `binding_message` | One short sentence the person reads before deciding |
| `requested_expiry` | Seconds the person has to answer. 120 if left out, 600 at most. |

2. The response has `auth_req_id`, `expires_in` and `interval`.
3. Poll the agent token endpoint with `grant_type=urn:openid:params:grant-type:ciba`, `auth_req_id` and a fresh client assertion, no more often than every `interval` seconds.

| Response | What the agent does |
| --- | --- |
| `400` `authorization_pending` | Waits `interval` seconds, polls again |
| `400` `slow_down` | Waits longer between polls |
| `400` `access_denied` | Stops |
| `400` `expired_token` | Stops, or asks again |
| `200` with an access token | Goes ahead |

In the token, `sub` is the person who approved, `act.sub` is the agent as `agent:agt_…`, and `scope` is what the person approved. The first successful poll spends the approval.

## Write a good binding message

It is the only thing the person reads before deciding, usually on a phone. Name the amount, the destination and the thing: "Merge pull request 482 into `main`", not "Approve agent request".

## Detail

- Request and response for each step, and opening an approval request directly: [Ask before a sensitive action](https://authfi.io/docs/agents/approvals)
- The full CIBA exchange: [Ask a named person to approve](https://authfi.io/docs/agents/ciba)
