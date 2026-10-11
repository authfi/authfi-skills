---
type: Concept
title: "Roles, groups and grants"
description: "The four things every AuthFI access decision is made from, and the order a decision is made in."
tags: [authfi, access, roles, groups, grants, permissions]
sources:
  - id: concepts-access
    resource: https://authfi.io/docs/concepts/access
    title: "Roles, groups and grants"
---

# Roles, groups and grants

## The four terms

| Term | What it is | Example |
| --- | --- | --- |
| Permission | An action on a kind of thing | `read:audit` |
| Role | A named set of permissions | Administrator, Auditor, Developer |
| Group | A set of people, agents and other groups | `engineering` |
| Grant | One subject's access to one particular thing | `group:engineering` may open `grafana` |

A role answers "what may this person do in the project?". A grant answers "may this person reach this one application, cloud role or server?".

A subject is written as its kind and its ID: `user:`, `group:`, `agent:` or `app:`.

## How a decision is made

1. If a rule denies it, the answer is no. Nothing overrides a deny.
2. Otherwise, if a role's permission or a grant allows it, the answer is yes.
3. If a rule says the action needs approval, a yes becomes "wait for a person".
4. If nothing allowed it, the answer is no.

## What this means for an integration

- **Give access to groups, and move people between groups.** Grant something to a group and every member has it. Groups can contain groups.
- **A change is seen everywhere within 30 seconds**, and at the latest when the current token expires.
- **Tokens carry `groups` and `roles` claims.** The `groups` claim lists only the groups assigned to the application or shared with it, not every group the person is in.
- **An application is open until first assigned.** Until a group is assigned, anyone who can sign in to the project can use it. The first assignment closes it to everyone else. A person who is not assigned gets `access_denied`.
- **Grants and role bindings can carry an end date.**

## Detail

Where each one is managed in the console, the built-in roles and the kinds of thing a grant can be on are in [Roles, groups and grants](https://authfi.io/docs/concepts/access).
