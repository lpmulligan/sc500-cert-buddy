#!/usr/bin/env python3
"""PreToolUse policy gate for SC-500 Cert Buddy (Claude Code hook).

WHY THIS EXISTS
---------------
A hook runs as *your* code, not the model's. If a guarantee has to hold,
you hook it; you do not put it in the prompt. Asking a prompt nicely to
"avoid destructive commands" works most of the time, which is the worst
possible failure mode. This gate is deterministic enforcement.

CONTRACT (Claude Code PreToolUse hook)
--------------------------------------
- Claude Code pipes a JSON event to STDIN before a tool runs.
- We inspect Bash commands only. Everything else is allowed untouched.
- To BLOCK, print a JSON decision to STDOUT and exit 0:
      {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                               "permissionDecision": "deny",
                               "permissionDecisionReason": "<why>"}}
- To ALLOW, exit 0 with no decision payload.
- Any uncaught exception would be disruptive, so we fail OPEN with a logged
  warning rather than crash the session. Fail-open is the right call for a
  study tool. A production gate guarding money or infrastructure should fail
  CLOSED instead. The choice is deliberate, so it is documented here.

Ported from claude-architect/hooks-example.py (enforce_refund_policy).
"""
from __future__ import annotations

import json
import re
import sys

# Patterns that should never run unattended inside a study repo. Each entry
# is (compiled_regex, human_reason). The first match wins and we report it.
_DESTRUCTIVE: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\brm\s+(-[a-zA-Z]*\s+)*-?[a-zA-Z]*[rf]"), "recursive or forced 'rm' delete"),
    (re.compile(r"\bgit\s+clean\s+-[a-zA-Z]*d"), "'git clean -d' wipes untracked files"),
    (re.compile(r"\bgit\s+reset\s+--hard"), "'git reset --hard' discards local work"),
    (re.compile(r"\b(mkfs|dd)\b"), "low-level disk write (mkfs/dd)"),
    (re.compile(r">\s*/dev/sd[a-z]"), "raw write to a block device"),
    (re.compile(r"\bchmod\s+-R\s+777\b"), "world-writable recursive chmod"),
    (re.compile(r":\(\)\s*\{.*\};\s*:"), "fork bomb"),
    (re.compile(r"\bsudo\b"), "privilege escalation with sudo"),
    (re.compile(r"\bcurl\b.*\|\s*(sh|bash)\b"), "pipe-from-internet straight into a shell"),
]


def _deny(reason: str) -> None:
    """Emit a deny decision and exit successfully (exit 0 + JSON)."""
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"Blocked by SC-500 Cert Buddy policy gate: {reason}. "
                "Run it by hand if you truly intend this."
            ),
        }
    }))
    sys.exit(0)


def main() -> None:
    raw = sys.stdin.read()
    try:
        event = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        # Malformed event -> fail open, do not block the user.
        sys.exit(0)

    if event.get("tool_name") != "Bash":
        sys.exit(0)  # Only Bash is in scope for this gate.

    command = (event.get("tool_input") or {}).get("command", "")
    if not isinstance(command, str):
        sys.exit(0)

    for pattern, reason in _DESTRUCTIVE:
        if pattern.search(command):
            _deny(reason)

    sys.exit(0)  # Allowed.


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # never crash the session over a guardrail
        sys.stderr.write(f"policy-gate hook warning (failing open): {exc}\n")
        sys.exit(0)
