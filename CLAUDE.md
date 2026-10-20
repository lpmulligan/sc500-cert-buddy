# CLAUDE.md

Guidance for **Claude Code** when working in this repository.

## What this is

**SC-500 Cert Buddy (Claude Code edition).** An agentic study companion for **Exam SC-500: Implementing End-to-End Security Controls for Cloud and AI Workloads**, the exam for **Microsoft Certified: Cloud and AI Security Engineer Associate**. It generates exam-realistic practice questions, brief hands-on security labs with a license and cost gate, and personalized study plans, all grounded in **Microsoft Learn** through the **Microsoft Learn MCP server**.

This project is an SC-500 adaptation of Tim Warner's AI-901 Cert Buddy for Claude Code (`timothywarner-org/ai901-cert-buddy-claude`), which was itself a Claude Code port of his GitHub Copilot "Cert Buddy". The structure and primitives are Tim's; the SC-500 content is new. See `README.md` for the full primitive map and credits.

There is no application to build. The artifacts are agent definitions, skills, slash commands, hooks, and MCP configuration.

## Where things live (Claude Code primitives)

| Primitive | Location |
| --- | --- |
| Memory (this file) | `CLAUDE.md` |
| Subagents | `.claude/agents/` |
| Slash commands | `.claude/commands/` |
| Agent Skills | `.claude/skills/` |
| Hooks | `.claude/settings.json` + `.claude/hooks/` |
| MCP servers | `.mcp.json` |
| Plugin packaging | `.claude-plugin/` |

## The grounding contract (non-negotiable)

1. **Microsoft Learn first.** Ground every fact about Microsoft Entra ID, Azure Key Vault, Azure Policy and RBAC, Azure Storage and Azure SQL security, Azure network security, Microsoft Defender for Cloud, Microsoft Defender XDR, Microsoft Sentinel, Microsoft Purview, Microsoft Security Copilot, and Microsoft Foundry security in **Microsoft Learn**, accessed through the MCP server `mslearn`.
2. Use `microsoft_docs_search` for breadth, then `microsoft_docs_fetch` for full-page detail, and `microsoft_code_sample_search` when Azure CLI, Azure PowerShell, Microsoft Graph PowerShell, Bicep, or KQL syntax accuracy matters.
3. **Cite a real Microsoft Learn URL** for every question and every lab. Never invent a URL. If you cannot ground a claim, say so and stop.
4. Pick objectives from `.claude/skills/_references/sc500-objective-domain.md` (a verbatim Microsoft Learn sync). License and cost tiers for every objective live in `.claude/skills/_references/sc500-lab-requirements.md`.

## SC-500 canonical facts

- **Exam:** SC-500, Implementing End-to-End Security Controls for Cloud and AI Workloads.
- **Certification:** Microsoft Certified: Cloud and AI Security Engineer Associate.
- **Skills measured date:** not published on the study guide page as of 2026-10-20. **Pass score:** 700.
- **Domains:** Manage identity, access, and governance (**20-25%**); Secure storage, databases, and networking (**25-30%**); Secure compute (**20-25%**); Manage and monitor security posture (**20-25%**).
- **Domain keys** (used by `/quiz`, `/plan`, and the cert-buddy MCP server): `identity`, `storage-network`, `compute`, `posture`.
- **Audience:** security engineers with practical Azure and hybrid administration experience (compute, network, and storage), strong familiarity with Microsoft Entra ID, and familiarity with Microsoft 365 administration.

## Hard rules the skills depend on

- **Two-phase question delivery.** Present the scenario, stem, and choices ONLY. Stop. Wait for the learner's answer. THEN reveal the correct letter, a two-sentence rationale per choice, and the Microsoft Learn URLs. Never reveal the answer in the same message as the question.
- **Answer-letter randomization.** The correct answer must be randomized across A, B, C, and D. Never default to one position.
- **Fictional-company randomization.** Use only the WWL-approved company list in `.claude/skills/_references/fictional-companies.md`. Use the entire company name on every mention. Do not default to Contoso, Ltd.
- **Keyless auth default.** All commands and code use Microsoft Entra ID sign-in (`az login`, `Connect-AzAccount`, `Connect-MgGraph` with least-privileged scopes, `DefaultAzureCredential`, or managed identities). No account keys, SQL passwords, or client secrets unless an objective explicitly covers that mechanism (for example, shared access signatures in objective 2.1.4).
- **License and cost gate.** Every lab opens with the requirement tiers for its objective, the trial option, and the cleanup step that stops the cost. Labs exist for every objective; premium-only objectives also get a no-license path.
- **Lab safety.** Labs run only against a dedicated lab tenant and subscription. Conditional Access policies exclude a break-glass account and start in Report-only mode.
- **Style precedence.** Exam items follow the **Microsoft Worldwide Learning Exam Writing Style Guide (WWL)**; prose follows the **Microsoft Writing Style Guide (MWSG)**. When they conflict in an item, WWL wins (no contractions; key names in ALL CAPS). Full rules in `.claude/skills/_references/wwl-style-guide.md`.

## Current Microsoft product names (silently map retired names)

Always use current names, even if the user types a retired one.

| Retired / legacy name | Current name |
| --- | --- |
| Azure Active Directory (Azure AD) | Microsoft Entra ID |
| Azure AD Identity Protection | Microsoft Entra ID Protection |
| Azure Security Center / Azure Defender | Microsoft Defender for Cloud |
| Azure Security Benchmark | Microsoft cloud security benchmark |
| Azure Sentinel | Microsoft Sentinel |
| Microsoft 365 Defender | Microsoft Defender XDR |
| Microsoft Cloud App Security (MCAS) | Microsoft Defender for Cloud Apps |
| Microsoft Copilot for Security | Microsoft Security Copilot |
| Azure Purview | Microsoft Purview |
| Azure Policy Guest Configuration | Azure Machine Configuration |
| Log Analytics agent (MMA, OMS agent) | Azure Monitor Agent |
| Azure AI Studio / Azure AI Foundry | Microsoft Foundry |

The full table lives in the **sc500-item-creator** skill. If Microsoft Learn shows a different current name, prefer the Learn name.

## How the agent and skills fit together

The **sc500-cert-buddy** subagent (`.claude/agents/sc500-cert-buddy.md`) is the orchestrator. It delegates to three skills based on the request:

- **sc500-item-creator** for practice questions.
- **sc500-lab-creator** for hands-on security labs.
- **sc500-study-planner** for personalized study plans.

The **grounding-verifier** subagent independently checks that generated content cites live Microsoft Learn URLs, grounds its license claims, and uses no retired product names. The **azure-principal-architect** subagent is an optional "pair architect" for lab design.

## Maintainer and credits

Maintained by Lawrence Mulligan (GitHub: `lpmulligan`). Based on AI-901 Cert Buddy by Tim Warner, TechTrainerTim.com. MIT licensed.

## Imported rules

@.claude/rules/grounding.md

## Project layout

Beyond the core `.claude/` primitives, this repository includes:

- A custom MCP server in `mcp-server/` (server id `cert-buddy`), built on the MCP Python SDK (FastMCP, 1.x). It exposes tools (`score_answer`, `validate_item`, `next_question`, `grade_lab`, and the optional `generate_item`), resources (`certbuddy://domains`, `certbuddy://progress`, `certbuddy://bank/{domain}`), and prompts (`quiz`, `exam`). It is the scoring and interaction layer; **Microsoft Learn remains the source of truth.**
- Two context hooks: `session-start.py` (**SessionStart**) and `prompt-context.py` (**UserPromptSubmit**), which keep the grounding and WWL rules in front of the model on every session and every prompt.
- A **Cert Coach** output style in `.claude/output-styles/`.
- A workspace MCP config at `.vscode/mcp.json` so the Microsoft Learn MCP is turnkey in VS Code as well as Claude Code.
- Hook commands use `python3` (macOS and Linux first). The `cert-buddy` MCP server runs from a repo venv at `mcp-server/.venv/bin/python3` (git-ignored; create it with `python3 -m venv mcp-server/.venv` and install `mcp-server/requirements.txt`). On Windows, change hooks to `python` or `py` and the MCP command to `mcp-server\.venv\Scripts\python.exe`.

## Turnkey grounding (non-negotiable)

The Microsoft Learn MCP connection **travels with this repository** in `.mcp.json` (Claude Code) and `.vscode/mcp.json` (VS Code). A clone is grounded out of the box with no API key. All SC-500 content is grounded **100 percent at Microsoft Learn first**, and every practice item follows the **Microsoft Worldwide Learning (WWL)** exam-writing rules. The agent and skills never substitute generic web search for Microsoft Learn.
