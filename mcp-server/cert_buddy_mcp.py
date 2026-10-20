"""cert-buddy-mcp -- a teaching MCP server for SC-500 Cert Buddy.

Built on the official Model Context Protocol Python SDK (FastMCP). It is a
local, no-network study server that showcases the three core MCP primitives in
one place:

  * tools     -- model-callable actions (score_answer, validate_item, next_question)
  * resources -- read-only context (certbuddy://domains, certbuddy://progress,
                 certbuddy://bank/{domain})
  * prompts   -- user-invocable templates that surface as slash commands in
                 Claude Code (/quiz, /exam)

It also includes ONE optional tool, generate_item, that calls Claude through the
Anthropic Python SDK to author a fresh practice item. That tool activates only
when ANTHROPIC_API_KEY is set; without a key the server still runs and the other
primitives work, so the repository always clones-and-runs.

GROUNDING NOTE: This server is the interaction and scoring layer. The source of
truth for SC-500 facts remains Microsoft Learn, reached through the
mslearn MCP server. Every item in data/question-bank.json carries
Microsoft Learn references, and the agent grounds new content at Microsoft Learn
first, per the Microsoft Worldwide Learning (WWL) exam-writing rules.

Run it standalone for development:
    python3 -m pip install -r requirements.txt
    python3 cert_buddy_mcp.py           # stdio transport

Claude Code launches it automatically via .mcp.json (server id: cert-buddy).
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

# --- Data layer -----------------------------------------------------------
HERE = Path(__file__).parent
BANK_PATH = HERE / "data" / "question-bank.json"

# SC-500 exam blueprint. Weights come from the public study guide; the keys
# match .claude/skills/_references/sc500-objective-domain.md.
DOMAINS: dict[str, dict[str, Any]] = {
    "identity": {
        "id": "identity",
        "title": "Manage identity, access, and governance",
        "weight": "20-25%",
    },
    "storage-network": {
        "id": "storage-network",
        "title": "Secure storage, databases, and networking",
        "weight": "25-30%",
    },
    "compute": {
        "id": "compute",
        "title": "Secure compute",
        "weight": "20-25%",
    },
    "posture": {
        "id": "posture",
        "title": "Manage and monitor security posture",
        "weight": "20-25%",
    },
}

# In-memory progress. A production build would persist this; for a teaching
# server we keep it in process so the progress resource has something honest
# to report during a session.
_PROGRESS: dict[str, dict[str, int]] = {
    key: {"seen": 0, "correct": 0} for key in DOMAINS
}


def _load_bank() -> list[dict[str, Any]]:
    """Load the original practice-item bank. Returns [] when the file is absent."""
    try:
        return json.loads(BANK_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"question-bank.json is not valid JSON: {exc}") from exc


def _get_item(item_id: int) -> dict[str, Any] | None:
    for item in _load_bank():
        if item.get("id") == item_id:
            return item
    return None


mcp = FastMCP("cert-buddy")

# --- Tools ----------------------------------------------------------------


@mcp.tool()
def score_answer(item_id: int, chosen: str) -> dict[str, Any]:
    """Grade a chosen letter (A-D) against a bank item.

    Returns whether the choice is correct plus the per-choice rationale, and
    updates in-memory progress for the item's domain. Use this to evaluate a
    learner's answer after they commit to a choice.
    """
    item = _get_item(item_id)
    if item is None:
        return {"isError": True, "message": f"No item with id {item_id}."}
    chosen = chosen.strip().upper()
    if chosen not in {"A", "B", "C", "D"}:
        return {"isError": True, "message": "chosen must be one of A, B, C, D."}

    correct = item["answer"]
    domain = item.get("domain", "unassigned")
    _PROGRESS.setdefault(domain, {"seen": 0, "correct": 0})
    _PROGRESS[domain]["seen"] += 1
    if chosen == correct:
        _PROGRESS[domain]["correct"] += 1

    return {
        "correct": chosen == correct,
        "chosen": chosen,
        "answer": correct,
        "rationale": item["rationale"],
        "references": item.get("references", []),
    }


@mcp.tool()
def validate_item(item: dict[str, Any]) -> dict[str, Any]:
    """Validate a practice item against SC-500 and WWL structural rules.

    Returns a STRUCTURED list of issues rather than prose, so an agentic loop
    can read the issues and repair the item. An empty issues list means valid.
    This is the structured-error pattern the repair step depends on.

    Stems are scenario-first, so the WWL question-sentence rules apply to the
    final sentence only. "do" is banned as an auxiliary ("Which service do you
    use?") but allowed as the main verb ("What should you do?").
    """
    issues: list[str] = []
    stem = str(item.get("stem", "")).strip()
    choices = item.get("choices", {})
    if not isinstance(choices, dict) or set(choices) != {"A", "B", "C", "D"}:
        issues.append("Item must have exactly four choices keyed A, B, C, D.")
    if item.get("answer") not in {"A", "B", "C", "D"}:
        issues.append("answer must be one of A, B, C, D.")
    if not stem.endswith("?"):
        issues.append("Stem must be a question ending in '?'.")
    # Final sentence: the text after the last sentence-ending punctuation.
    question = re.split(r"(?<=[.?!])\s+", stem)[-1] if stem else ""
    if not re.match(r"(What|Which)\b", question):
        issues.append("Question sentence must begin with 'What' or 'Which' (WWL).")
    if not re.search(r"\bshould\b", question, re.IGNORECASE):
        issues.append("Question sentence must use 'should' as the auxiliary (WWL).")
    for banned in ("can", "must", "might", "may", "would"):
        if re.search(rf"\b{banned}\b", question, re.IGNORECASE):
            issues.append(f"Question uses banned auxiliary '{banned}'; use 'should' (WWL).")
    if re.search(r"\b(do|does|did)\s+(you|we|they|i|the|a|an)\b", question, re.IGNORECASE):
        issues.append("Question uses 'do' as an auxiliary; use 'should' (WWL).")
    rationale = item.get("rationale", {})
    if isinstance(choices, dict) and set(rationale) != set(choices):
        issues.append("Provide a rationale for every choice.")
    return {"valid": not issues, "issues": issues}


@mcp.tool()
def next_question(domain: str = "") -> dict[str, Any]:
    """Return the next practice item, Phase 1 only (stem and choices).

    Picks from the requested domain, or rotates across the bank when no domain
    is given. The correct answer and rationale are withheld on purpose; call
    score_answer after the learner commits to a choice.
    """
    bank = _load_bank()
    if not bank:
        return {"isError": True, "message": "Question bank is empty."}
    pool = [i for i in bank if not domain or i.get("domain") == domain]
    if not pool:
        return {"isError": True, "message": f"No items for domain '{domain}'."}
    if domain:
        seen = _PROGRESS.get(domain, {}).get("seen", 0)
    else:
        seen = sum(p["seen"] for p in _PROGRESS.values())
    item = pool[seen % len(pool)]
    return {
        "id": item["id"],
        "domain": item["domain"],
        "objective": item.get("objective", ""),
        "stem": item["stem"],
        "choices": item["choices"],
        "note": "Phase 1 only. Call score_answer with your chosen letter to reveal the answer.",
    }


@mcp.tool()
def generate_item(domain: str = "storage-network", topic: str = "") -> dict[str, Any]:
    """Author a fresh SC-500 item with Claude (optional, needs ANTHROPIC_API_KEY).

    This is the Anthropic-SDK showcase. When ANTHROPIC_API_KEY is set, it asks
    Claude to write one original, WWL-styled item as JSON. When the key is
    absent, it returns a clear, non-failing message so the server still runs.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {
            "isError": True,
            "message": "generate_item needs ANTHROPIC_API_KEY. The rest of the "
            "server runs without it; set the key to enable live authoring.",
        }
    try:
        import anthropic  # imported lazily so the dependency stays optional
    except ImportError:
        return {"isError": True, "message": "Install the 'anthropic' package to use generate_item."}

    client = anthropic.Anthropic(api_key=api_key)
    system = (
        "You are an SC-500 exam item writer. Write ONE original multiple-choice "
        "item as strict JSON with keys: domain, objective, stem, choices (A-D), "
        "answer, rationale (A-D), references. The stem is a scenario question "
        "ending in '?', starts with What or Which, uses 'should', no "
        "contractions, current Microsoft product names only (Microsoft Entra ID, "
        "Microsoft Defender for Cloud, Microsoft Sentinel, Microsoft Defender XDR). "
        "State any license or plan the correct answer depends on. Ground claims "
        "in Microsoft Learn. Output JSON only."
    )
    if domain not in DOMAINS:
        return {"isError": True, "message": f"domain must be one of {sorted(DOMAINS)}."}
    user = f"Domain: {DOMAINS[domain]['title']}. Topic focus: {topic or 'any in-scope objective'}."
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    text = "".join(block.text for block in message.content if block.type == "text")
    try:
        return {"item": json.loads(text)}
    except json.JSONDecodeError:
        return {"isError": True, "message": "Model did not return valid JSON.", "raw": text}


@mcp.tool()
def grade_lab(answer_key: dict[str, Any], submission: dict[str, Any]) -> dict[str, Any]:
    """Grade a lab submission against a canonical answer key.

    answer_key follows labs/README.md: a total_points integer and a checks list
    of {id, description, expected, points, requires_license?}. submission maps
    each check id to the value the learner observed. When submission contains
    "_path": "no-license", checks marked requires_license are left out of the
    score. Comparison is case-insensitive and trimmed, so the grading stays
    transparent and easy to audit and extend.
    """
    checks = answer_key.get("checks", [])
    if not isinstance(checks, list) or not checks:
        return {"isError": True, "message": "answer_key.checks must be a non-empty list."}

    def _norm(value: Any) -> str:
        return str(value).strip().casefold()

    no_license = str(submission.get("_path", "")).strip().casefold() == "no-license"

    results: list[dict[str, Any]] = []
    skipped: list[str] = []
    earned = 0
    possible = 0
    for check in checks:
        cid = check.get("id")
        if no_license and check.get("requires_license"):
            skipped.append(cid)
            continue
        points = int(check.get("points", 0))
        possible += points
        submitted = submission.get(cid)
        passed = submitted is not None and _norm(submitted) == _norm(check.get("expected"))
        if passed:
            earned += points
        results.append({
            "id": cid,
            "description": check.get("description", ""),
            "expected": check.get("expected"),
            "submitted": submitted,
            "points": points,
            "passed": passed,
        })

    total = possible if no_license else (answer_key.get("total_points") or possible)
    percent = round(100 * earned / total, 1) if total else 0.0
    return {
        "earned_points": earned,
        "total_points": total,
        "percent": percent,
        "passed_count": sum(1 for r in results if r["passed"]),
        "check_count": len(results),
        "skipped_requires_license": skipped,
        "results": results,
    }


# --- Resources ------------------------------------------------------------


@mcp.resource("certbuddy://domains")
def domains_resource() -> str:
    """The SC-500 exam blueprint: the four domains and their weights."""
    return json.dumps(list(DOMAINS.values()), indent=2)


@mcp.resource("certbuddy://progress")
def progress_resource() -> str:
    """In-session progress: items seen and correct, per domain."""
    return json.dumps(_PROGRESS, indent=2)


@mcp.resource("certbuddy://bank/{domain}")
def bank_resource(domain: str) -> str:
    """The Phase-1 view (no answers) of the question bank for one domain."""
    items = [
        {k: v for k, v in i.items() if k not in {"answer", "rationale"}}
        for i in _load_bank()
        if i.get("domain") == domain
    ]
    return json.dumps(items, indent=2)


# --- Prompts (surface as slash commands in Claude Code) -------------------


@mcp.prompt()
def quiz(domain: str = "") -> str:
    """Start a two-phase quiz on an SC-500 domain."""
    where = f"the '{domain}' domain" if domain else "a weighted mix of all four domains"
    return (
        f"Quiz me on {where}. Call next_question to get one item, show me the "
        "stem and choices only, wait for my answer, then call score_answer and "
        "reveal the rationale with Microsoft Learn references."
    )


@mcp.prompt()
def exam(count: int = 5) -> str:
    """Run a short mock exam of N items with an end summary."""
    return (
        f"Give me a {count}-item SC-500 mock exam. For each item call "
        "next_question, collect my answer, then score_answer. Track a running "
        "score and finish with a per-domain summary and what to review next."
    )


if __name__ == "__main__":
    # stdio transport: Claude Code speaks to this over stdin/stdout.
    mcp.run()
