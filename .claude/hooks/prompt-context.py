#!/usr/bin/env python3
"""UserPromptSubmit hook -- keep grounding and style rules in front of the model.

Fires on every user prompt. It adds a compact reminder so the buddy never drifts
from the two rules that matter most: ground at Microsoft Learn first, and write
exam items to the WWL guidelines with current product names. Never raises.
"""
from __future__ import annotations

import json
import sys

REMINDER = (
    "Reminder: ground claims in Microsoft Learn first (mslearn). "
    "For practice items, follow WWL (begin with What or Which, use should, no "
    "contractions, randomize the answer letter and the fictional company) and "
    "use only current Microsoft product names."
)


def main() -> None:
    # Read and ignore the event payload; this hook adds context unconditionally.
    sys.stdin.read()
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": REMINDER,
        }
    }))


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit(0)
