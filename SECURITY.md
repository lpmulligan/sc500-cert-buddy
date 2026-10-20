# Security Policy

## Scope

This repository contains Claude Code agent definitions, Agent Skills, slash
commands, hook scripts, and an MCP server configuration for SC-500
certification study. It does not contain application code, backend services, or
deployable software.

The `mslearn` server in `.mcp.json` is a public Microsoft Learn HTTP endpoint
that requires no API key. The `cert-buddy` server is a local stdio process. No secrets are hardcoded in any tracked file. The
`.gitignore` file excludes `.env` files, private keys, and the runtime
`.cert-buddy/` audit directory from version control.

## Reporting a vulnerability

If you discover a security issue in this repository, please report it by email:

- **To:** <lmulligan@lpmnet.com>
- **Subject line:** Security: sc500-cert-buddy
- **Include:** A clear description of the issue, the affected file or files, and
  steps to reproduce the problem if applicable.

You can expect an initial response within 48 hours.

## What counts as a security issue

- **Hardcoded secrets or API keys** in any tracked file (subagents, skills,
  commands, hooks, MCP config, or reference documents).
- **MCP or hook configurations that could leak credentials**, such as a hook
  that writes secrets to `.cert-buddy/audit.log` or an MCP server that passes a
  token as a visible command-line argument.
- **Prompt injection vulnerabilities** in subagent, skill, or command
  definitions that could cause the agent to bypass its safety rules, exfiltrate
  context, or take unintended actions.
- **Hook scripts that fail unsafely**, for example a `PreToolUse` gate that can
  be trivially bypassed when it is supposed to block an action.
- **References to real exam content** that compromise the integrity of the
  Microsoft SC-500 certification exam. This repository must contain only
  original practice material.

## What is NOT a security issue

Report these through regular GitHub Issues instead:

- Feature requests or suggestions for new content.
- Outdated terminology or product name changes.
- General documentation improvements.

## A note on the hooks

The hook scripts in `.claude/hooks/` run as local Python on your machine when
Claude Code fires the matching event. Read them before you trust them. They are
small and dependency-free on purpose:

- `policy-gate.py` reads a tool event on standard input and denies destructive
  Bash commands. It fails open, which is the right default for a study tool but
  the wrong default for a gate guarding money or infrastructure.
- `citation-audit.py` appends Microsoft Learn lookups to `.cert-buddy/audit.log`
  and never blocks or raises.

## Responsible disclosure

Please do not publicly disclose a security issue until it has been reviewed and
addressed. If you have not received a response within 48 hours, send a follow-up
email to the same address.

## Maintainer

- **Name:** Lawrence Mulligan
- **GitHub:** [@lpmulligan](https://github.com/lpmulligan)
- **Email:** <lmulligan@lpmnet.com>
