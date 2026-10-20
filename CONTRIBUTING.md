# Contributing to SC-500 Cert Buddy (Claude Code Edition)

Thank you for your interest in contributing. SC-500 Cert Buddy is an educational resource that helps people prepare for Exam SC-500 (Microsoft Certified: Cloud and AI Security Engineer Associate) using Claude Code. Contributions of all kinds are welcome, whether you are fixing a typo, updating terminology, proposing a new skill, or improving reference material.

## How to contribute

### Report issues

If you find something incorrect, outdated, or broken, please open a GitHub issue. Common examples include:

- **Outdated terminology** -- a retired product name that should use the current Microsoft name (for example, "Azure Security Center" should be "Microsoft Defender for Cloud").
- **Incorrect behavior** -- a question rationale or lab step that does not match current Microsoft Entra, Azure, Defender, Sentinel, or Purview functionality.
- **Outdated licensing** -- a lab license and cost gate that no longer matches Microsoft Learn (licensing changes often).
- **Broken MCP configuration** -- a server definition in `.mcp.json` that fails to connect.
- **Inaccurate references** -- a Microsoft Learn URL that no longer resolves or points to the wrong topic.

When opening an issue, include enough detail to locate and reproduce the problem (file path, line number, expected versus actual behavior).

### Suggest new skills, commands, or subagents

Have an idea for a new Agent Skill, slash command, or subagent? Open an issue describing what it would do, which SC-500 objective it covers, and how it differs from the existing pieces.

### Improve reference documents

The `.claude/skills/_references/` directory contains supporting material:

- `sc500-objective-domain.md` -- the SC-500 skills-measured reference.
- `sc500-lab-requirements.md` -- the license and cost tier for every objective.
- `wwl-style-guide.md` -- the exam-writing style rules.
- `fictional-companies.md` -- approved fictional company names, cities, and resource conventions.

If any of these are out of date, submit a pull request with corrections.

## Contribution guidelines

All contributions must follow these rules. They are the same rules the buddy itself enforces.

### Terminology

Always use current Microsoft product names. Never use a retired name, even when quoting user-facing text. Common renames:

| Retired name | Current name |
| --- | --- |
| Azure Active Directory (Azure AD) | Microsoft Entra ID |
| Azure Security Center / Azure Defender | Microsoft Defender for Cloud |
| Azure Sentinel | Microsoft Sentinel |
| Microsoft 365 Defender | Microsoft Defender XDR |
| Microsoft Copilot for Security | Microsoft Security Copilot |
| Azure Policy Guest Configuration | Azure Machine Configuration |
| Log Analytics agent (MMA, OMS agent) | Azure Monitor Agent |
| Azure AI Studio / Azure AI Foundry | Microsoft Foundry |

If Microsoft Learn shows a different current name than what appears above, prefer the Learn name. The working rename table lives in `CLAUDE.md`.

### Writing style

- **No contractions** in generated content or instructions. Write "do not" instead of "don't," "cannot" instead of "can't."
- **Plain ASCII only.** Do not use curly quotes, en dashes, or em dashes. Use straight quotes and double hyphens (`--`).
- **Microsoft style formatting.** Use **bold** for UI labels and sentence-style capitalization for headings.
- **Avoid negatives** unless required. When a negative word is necessary, capitalize and bold it (for example, **NOT**).

### Content integrity

- **Questions must be original.** Do not copy, paraphrase, or reference real exam questions or leaked content.
- **Distractors must be real.** Wrong answer choices must reference actual Microsoft security services, roles, and plans, never invented ones.
- **Labs must include cleanup steps.** Every lab must end by removing the resources it created and turning off the plans it enabled.
- **Labs must open with a license and cost gate.** Ground every license claim in Microsoft Learn.
- **All claims must be groundable in Microsoft Learn.** If you cannot find a supporting reference on Microsoft Learn, do not include the claim.

## File conventions

### Subagent files

Subagents live in `.claude/agents/<name>.md`. Each file has YAML frontmatter with at least `name` and `description`, an optional scoped `tools` list, and a Markdown body. Keep the `tools` list as small as the job allows.

### Slash command files

Slash commands live in `.claude/commands/<name>.md` and are invoked as `/<name>`. Frontmatter may include `description`, `argument-hint`, and `allowed-tools`. Use `$ARGUMENTS` for input.

### Skill files

Skills live in `.claude/skills/<skill-name>/SKILL.md` with YAML frontmatter (`name`, `description`) and a Markdown body. The `name` field is the canonical identifier.

### MCP and hooks

Tool IDs in subagents and commands must match the server ID in `.mcp.json` (`mslearn`). Hooks are registered in `.claude/settings.json` and implemented in `.claude/hooks/`.

## Pull request process

1. **Fork** and create a feature branch from `main` with a descriptive name.
2. **Keep changes focused.** One skill, command, or fix per pull request.
3. **Describe what you changed and why.**
4. **Verify product names** against the terminology table above.
5. **Check ASCII compliance** (no curly quotes or dashes).
6. **Match tool IDs** to the server ID in `.mcp.json`.

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating, you agree to uphold it. In short: be respectful, be constructive, and be supportive of learners at all levels.

## Questions

- **Name:** Lawrence Mulligan
- **GitHub:** [@lpmulligan](https://github.com/lpmulligan)
- **Email:** <lmulligan@lpmnet.com>

This project builds on AI-901 Cert Buddy by Tim Warner ([TechTrainerTim.com](https://TechTrainerTim.com)). Thank you for helping make SC-500 Cert Buddy a better resource for everyone preparing for the Cloud and AI Security Engineer Associate certification.
