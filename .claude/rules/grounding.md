# Grounding and style rules (imported into memory)

This file is imported into project memory from `CLAUDE.md`. It holds the rules
that must never drift, kept in one place so they are easy to audit and reuse.

## Ground at Microsoft Learn first

- Ground every SC-500 fact in **Microsoft Learn**, reached through the
  `mslearn` MCP server, before any other source.
- Use `microsoft_docs_search` for breadth, `microsoft_docs_fetch` for detail,
  and `microsoft_code_sample_search` for SDK, CLI, or Bicep accuracy.
- Cite a real Microsoft Learn URL for every question and lab. Never invent a
  URL. If a claim cannot be grounded, say so and stop.

## Microsoft Worldwide Learning (WWL) exam-writing rules

- Begin a question with **What** or **Which**, and use **should** as the
  auxiliary. Do not use can, must, may, would, or do in the question sentence.
- No contractions. Use current Microsoft product names only.
- Randomize the correct answer across A, B, C, and D, and randomize the
  fictional company across the approved list.
- Distractors must reference real Microsoft security services, features,
  roles, and plans, never invented ones.
- Deliver questions in two phases: stem and choices first, then the rationale
  and references after the learner answers.

## Keyless by default

- All commands and code use Microsoft Entra ID sign-in (`az login`,
  `Connect-AzAccount`, `Connect-MgGraph` with least-privileged scopes,
  `DefaultAzureCredential`, or managed identities). No account keys, SQL
  passwords, or client secrets unless an objective explicitly covers that
  mechanism, such as shared access signatures in objective 2.1.4.

## Licenses and lab safety

- Every lab opens with a license and cost gate from
  `.claude/skills/_references/sc500-lab-requirements.md`, re-grounded in
  Microsoft Learn, because licensing changes often.
- Labs run only against a dedicated lab tenant and subscription. Conditional
  Access policies exclude a break-glass account and start in Report-only mode.
