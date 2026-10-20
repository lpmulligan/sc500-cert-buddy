#!/usr/bin/env python3
"""SessionStart hook -- prime every SC-500 study session.

Claude Code fires SessionStart when a session begins. This hook returns a short
additionalContext block so the model starts every session knowing the ground
rules. Pure standard library, never raises.
"""
from __future__ import annotations

import json
import sys

CONTEXT = (
    "SC-500 Cert Buddy is loaded. Commands: /quiz, /lab, /plan, /explain, /grade. "
    "Ground every answer in Microsoft Learn through the mslearn MCP server, use "
    "current Microsoft product names, follow the Microsoft Worldwide Learning "
    "(WWL) exam-writing rules for any practice item, and open every lab with "
    "its license and cost gate."
)


def main() -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": CONTEXT,
        }
    }))


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit(0)
