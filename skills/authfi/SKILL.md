---
name: authfi
type: Skill
title: "AuthFI for integrators"
description: "Use when a developer starts integrating an app, a service, an AI agent or a Kubernetes workload with AuthFI, asks what a project or an issuer is, or needs to pick the right AuthFI skill for the job."
tags: [authfi, identity, oidc, discovery, getting-started]
sources:
  - id: docs-home
    resource: https://authfi.io/docs/
    title: "AuthFI documentation"
  - id: concepts-projects
    resource: https://authfi.io/docs/concepts/projects
    title: "Projects and issuers"
  - id: concepts-access
    resource: https://authfi.io/docs/concepts/access
    title: "Roles, groups and grants"
---

# AuthFI for integrators

AuthFI is an identity platform for people and AI agents. You work in a **project**: one complete identity provider at one URL, for example `https://acme.authfi.io`. Applications sign people in through it, AI agents get their own identity and limits from it, and Zero-Code puts its sign-in in front of services already running on Kubernetes.

## Rules that apply every time

1. **The issuer is the only value you configure.** A project's URL, `https://<project>.authfi.io`, is its issuer and the `iss` of every token it signs. Ask the developer for it. Never guess it.
2. **Read endpoints from discovery. Do not hard-code them.** An OpenID Connect library needs only the issuer. See [projects-and-discovery.md](projects-and-discovery.md).
3. **Projects are separate.** They share no people, keys or tokens. A token from one project does not verify against the keys of another. A company usually has more than one project, for example one for production and one for testing.
4. **Use a library for the standard.** Where AuthFI implements a published standard, the docs name it, so any library for that standard works. Reach for one before writing protocol code by hand.
5. **Find signing keys by `kid`.** Cache the key set, fetch it again on an unknown `kid`, and never pin one key.
6. **Access is denied by default and given to groups.** Do not design around per-person grants. See [access-model.md](access-model.md).
7. **Use the docs' words.** Project, issuer, application, client ID, redirect URI, sign in, AI agent, MCP gateway.
8. **Do not state what the docs do not.** When a detail is missing here, open the linked docs page. Every docs page is also plain Markdown: add `.md` to its URL. The list of all pages is at `https://authfi.io/docs/llms.txt`.

The docs examples use a project called `acme`. Replace `acme.authfi.io` with the developer's own issuer.

## Which skill to load

| The developer wants to | Load |
| --- | --- |
| Sign a person in to a web, browser or native app | `authfi-sign-in` |
| Get a token for a backend service with no person | `authfi-machine-to-machine` |
| Give an AI agent an identity, limits or approvals, or accept agents at an API | `authfi-agent-auth` |
| Let an agent call tools through the project's MCP gateway | `authfi-mcp-gateway` |
| Put sign-in or token checks in front of a Kubernetes service without changing it | `authfi-zero-code` |
| Validate a token, read a claim or handle an error code | `authfi-tokens-and-errors` |

## Files in this skill

| File | Read it when |
| --- | --- |
| [projects-and-discovery.md](projects-and-discovery.md) | You need an endpoint, the key set or a discovery document |
| [access-model.md](access-model.md) | You need to know who may do what, or why a caller was denied |

## Docs

- Documentation home: <https://authfi.io/docs/>
- Glossary: <https://authfi.io/docs/glossary>
