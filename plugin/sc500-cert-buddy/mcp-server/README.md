# cert-buddy-mcp

A small teaching MCP server for SC-500 Cert Buddy, built on the official **Model Context Protocol Python SDK (FastMCP)**. It showcases the three core MCP primitives in one place, and it adds one optional tool that uses the **Anthropic Python SDK**.

Claude Code launches it automatically through the project `.mcp.json` (server id `cert-buddy`). You can also run it standalone for development.

## What it exposes

| Primitive | Name | Purpose |
| --- | --- | --- |
| **Tool** | `score_answer` | Grade a chosen letter (A-D) against a bank item and update progress |
| **Tool** | `validate_item` | Check an item against SC-500 and WWL rules; returns a structured issue list |
| **Tool** | `next_question` | Return the next item, Phase 1 only (stem and choices, no answer) |
| **Tool** | `grade_lab` | Grade a lab submission against its answer key; supports the no-license path |
| **Tool** | `generate_item` | Author a fresh item with Claude (optional; needs `ANTHROPIC_API_KEY`) |
| **Resource** | `certbuddy://domains` | The SC-500 blueprint: the four domains and weights |
| **Resource** | `certbuddy://progress` | In-session progress per domain |
| **Resource** | `certbuddy://bank/{domain}` | Phase-1 view of the bank for one domain (templated URI) |
| **Prompt** | `quiz` | Two-phase quiz on a domain (surfaces as a slash command) |
| **Prompt** | `exam` | Short mock exam with an end summary |

## Grounding

This server is the interaction and scoring layer. The source of truth for SC-500 facts is **Microsoft Learn**, reached through the `mslearn` MCP server. Every item in `data/question-bank.json` carries Microsoft Learn references, and the agent grounds new content at Microsoft Learn first, following the Microsoft Worldwide Learning (WWL) exam-writing rules.

## Run it standalone

```bash
cd mcp-server
python3 -m pip install -r requirements.txt
python3 cert_buddy_mcp.py
```

To enable the optional `generate_item` tool, set a key first:

```bash
# macOS / Linux
export ANTHROPIC_API_KEY=sk-ant-...
# Windows PowerShell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

Without the key, the server still starts and every other primitive works. `generate_item` returns a clear message asking for the key.

## Files

```text
mcp-server/
  cert_buddy_mcp.py        FastMCP server (tools, resources, prompts)
  requirements.txt         mcp 1.x (required), anthropic (optional)
  data/
    question-bank.json     Original SC-500 items, each with Microsoft Learn references
  README.md                This file
```
