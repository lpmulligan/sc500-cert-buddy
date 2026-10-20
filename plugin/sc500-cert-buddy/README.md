# sc500-cert-buddy (plugin package)

This folder is the installable Claude Code plugin form of SC-500 Cert Buddy. It is **generated** from the project's single source of truth in `../../.claude/` and `../../mcp-server/` by `scripts/build-plugin.sh` (or `build-plugin.ps1`). Do not edit files here by hand; edit the project primitives and re-run the build script.

## What it bundles

- `agents/` -- the cert-buddy orchestrator, grounding-verifier, and azure-principal-architect subagents.
- `commands/` -- `/quiz`, `/lab`, `/plan`, `/explain`, `/grade`.
- `skills/` -- item creator, lab creator, study planner, with their references (objective domain, lab requirements matrix, WWL rules, fictional companies).
- `hooks/` -- the four hook scripts plus `hooks.json` (rooted at `${CLAUDE_PLUGIN_ROOT}`).
- `mcp-server/` -- the FastMCP server (tools, resources, prompts).
- `.mcp.json` -- the Microsoft Learn MCP and the local cert-buddy server.

## Install

```text
/plugin marketplace add lpmulligan/sc500-cert-buddy
/plugin install sc500-cert-buddy
```

The local server needs its dependency once: `python3 -m pip install -r mcp-server/requirements.txt`. The hooks and server run with `python3`; on Windows, edit `hooks/hooks.json` and `.mcp.json` to use `python` or `py`.
