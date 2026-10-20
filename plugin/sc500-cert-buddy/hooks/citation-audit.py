#!/usr/bin/env python3
"""PostToolUse citation audit for SC-500 Cert Buddy (Claude Code hook).

WHY THIS EXISTS
---------------
The buddy promises every answer is grounded in Microsoft Learn. A promise in
a prompt is a hope. This hook turns it into evidence: every call to the
Microsoft Learn MCP server is logged to .cert-buddy/audit.log with the query
and the URLs that came back. Now "it is grounded" is something you can open
and read, not something you take on faith.

CONTRACT (Claude Code PostToolUse hook)
---------------------------------------
- Claude Code pipes a JSON event to STDIN after a tool returns.
- The event includes tool_name, tool_input, and tool_response.
- An audit hook NEVER blocks and NEVER raises. An audit hook that throws is an
  audit hook that silently disables itself the first time it sees something
  unexpected. Log loudly, return quietly. Exit 0, always.

Ported from claude-architect/hooks-example.py (audit_tool_call).
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone

_URL_RE = re.compile(r"https?://[^\s\"'<>)\]]+")


def _project_dir() -> str:
    """Claude Code exports the project root to hooks. Fall back to cwd."""
    return os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())


def _flatten(obj: object) -> str:
    """Flatten a tool_response of unknown shape into searchable text."""
    try:
        return json.dumps(obj, ensure_ascii=False)
    except (TypeError, ValueError):
        return str(obj)


def main() -> None:
    raw = sys.stdin.read()
    try:
        event = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return  # Nothing to audit.

    tool = event.get("tool_name", "")
    if not tool.startswith("mcp__mslearn__"):
        return  # Only audit Microsoft Learn grounding calls.

    tool_input = event.get("tool_input") or {}
    response_text = _flatten(event.get("tool_response"))
    urls = sorted(set(_URL_RE.findall(response_text)))

    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "tool": tool,
        "query": tool_input.get("query") or tool_input.get("url") or tool_input,
        "url_count": len(urls),
        "urls": urls[:25],  # cap line length; the full set is rarely needed
        "session_id": event.get("session_id"),
    }

    audit_dir = os.path.join(_project_dir(), ".cert-buddy")
    os.makedirs(audit_dir, exist_ok=True)
    with open(os.path.join(audit_dir, "audit.log"), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit(0)  # A PostToolUse audit must never alter control flow.
