# AuthFI skills

Skills that teach a coding assistant how to integrate an application with [AuthFI](https://authfi.io/docs/), the identity platform for people and AI agents. They are for developers who use Claude Code, Cursor, Codex or another assistant that reads skills.

Each skill holds the rules that apply every time, the common pitfalls, and short task files that link to the AuthFI documentation for detail. Everything here is written from the public documentation at <https://authfi.io/docs/>.

## Install

All skills, installed globally for Claude Code:

```bash
npx skills add authfi/authfi-skills -g -a claude-code -y
```

One skill:

```bash
npx skills add authfi/authfi-skills -g -a claude-code -y --skill authfi-sign-in
```

By hand:

```bash
git clone https://github.com/authfi/authfi-skills.git
cp -r authfi-skills/skills/*/ ~/.claude/skills/
```

## Skills

| Skill | Use it when |
| --- | --- |
| [`authfi`](skills/authfi/SKILL.md) | You are starting an integration. What a project and an issuer are, discovery, the access model, and which skill to load. |
| [`authfi-sign-in`](skills/authfi-sign-in/SKILL.md) | You are signing people in with OpenID Connect, or handling redirect URIs, refresh tokens, sign-out or MFA. |
| [`authfi-machine-to-machine`](skills/authfi-machine-to-machine/SKILL.md) | A backend service needs an access token for another API. |
| [`authfi-agent-auth`](skills/authfi-agent-auth/SKILL.md) | An AI agent needs its own identity, limits or approvals, or your API accepts agent tokens. |
| [`authfi-mcp-gateway`](skills/authfi-mcp-gateway/SKILL.md) | An agent calls tools through your project's MCP gateway. |
| [`authfi-zero-code`](skills/authfi-zero-code/SKILL.md) | You are protecting a Kubernetes service without changing its code. |
| [`authfi-tokens-and-errors`](skills/authfi-tokens-and-errors/SKILL.md) | You are validating a token, reading a claim or handling an error code. |

## Layout

The `skills/` folder is an Open Knowledge Format (OKF v0.2) bundle. Each skill folder has a `SKILL.md`, an `index.md` that lists its files, and one file per topic. Every file names the documentation pages it was written from in its `sources`.

To check the bundle:

```bash
python scripts/okf_validate.py
```

## Documentation

- AuthFI documentation: <https://authfi.io/docs/>
- Every page as plain Markdown: add `.md` to its URL
- The list of all pages: <https://authfi.io/docs/llms.txt>

## License

MIT. See [LICENSE](LICENSE).
