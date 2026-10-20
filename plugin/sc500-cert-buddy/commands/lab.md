---
description: Build a hands-on SC-500 security lab and SAVE it as a gradable document (instructions plus a canonical answer key), with a license and cost gate up front.
argument-hint: "[objective number or topic, e.g. '3.2.3' or 'JIT VM access']; leave blank for a short menu of lab topics"
allowed-tools: Read, Write, Grep, Glob, mcp__mslearn__microsoft_docs_search, mcp__mslearn__microsoft_docs_fetch, mcp__mslearn__microsoft_code_sample_search
---

Use the **sc500-lab-creator** skill to build a short, hands-on SC-500 lab on: $ARGUMENTS

## If no topic is given, offer a pick-list

Show one lab topic per SC-500 domain, plus one AI security topic, and label each with its requirement tier from `.claude/skills/_references/sc500-lab-requirements.md` so the learner can see what it needs before picking. For example:

- **identity** -- 1.3.1 Enforce a security control with a custom Azure Policy definition (`FREE`)
- **storage-network** -- 2.3.6 Secure a storage account with a private endpoint (`PAYG`)
- **compute** -- 3.2.3 Enforce just-in-time VM access (`TRIAL`, Defender for Servers Plan 2)
- **ai-security** -- 3.1.7 Deploy AI Gateway in API Management for Microsoft Foundry (`PAYG`)
- **posture** -- 4.2.8 Automate incident response with a Sentinel automation rule (`TRIAL`)

Let the learner pick, or choose one and say which. Any objective number from `.claude/skills/_references/sc500-objective-domain.md` is valid, including the ones that need a premium license.

## Emit a gradable lab document

Save the lab under `labs/<slug>/` as TWO files so it can be auto-graded later with `/grade`:

1. `labs/<slug>/lab.md` -- the learner-facing lab: the license and cost gate, objective, prerequisites (a dedicated lab tenant and subscription), numbered steps (Microsoft Entra ID sign-in with least-privileged scopes), validation gates, the no-license path when the objective needs a premium license, troubleshooting, and a mandatory cleanup step.
2. `labs/<slug>/answer-key.json` -- the canonical answer key a grader compares against. Follow the schema in [`labs/README.md`](../../labs/README.md): a `checks` array where each entry has `id`, `description`, `expected`, `points`, and optionally `requires_license`, plus a `total_points` field.

Ground every step, service name, license claim, and command in Microsoft Learn first, and cite the URLs in `lab.md`. When done, tell the learner where the two files were saved and that they can run `/grade <slug>` once they have recorded their results in `labs/<slug>/submission.json`.
