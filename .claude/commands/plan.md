---
description: Build a personalized SC-500 study plan from your confidence ratings across the four exam domains and the licenses you can lab with.
argument-hint: "(optional) e.g. 'identity=strong storage-network=weak compute=moderate posture=unknown' (levels: strong|moderate|weak|unknown)"
allowed-tools: Read, Grep, Glob, mcp__mslearn__microsoft_docs_search, mcp__mslearn__microsoft_docs_fetch
---

Use the **sc500-cert-buddy** subagent and the **sc500-study-planner** skill to build a personalized SC-500 study plan.

Starting input (optional): $ARGUMENTS

## If no ratings are given, show the pick-list

Present the four SC-500 domains with their exam weights, and ask the learner to rate each on a simple scale, explained in plain language:

- **Domain 1** (`identity`) -- Manage identity, access, and governance (20-25%)
- **Domain 2** (`storage-network`) -- Secure storage, databases, and networking (25-30%)
- **Domain 3** (`compute`) -- Secure compute, including security for AI (20-25%)
- **Domain 4** (`posture`) -- Manage and monitor security posture (20-25%)

Confidence levels:

- `strong` -- configures this in production, needs light review only
- `moderate` -- understands it, needs targeted hands-on practice
- `weak` -- limited experience, needs focused study
- `unknown` -- not sure, treat as weak

Also ask which licenses the learner can lab with (an Azure subscription, Microsoft Entra ID P1 or P2, Microsoft 365 E5, Microsoft Agent 365, Security Copilot capacity), so the plan can mark which areas are lab-ready.

## Then plan

1. Order study from weakest to strongest; within equal confidence, prioritize the higher-weight domain.
2. For each area give estimated hours, current Microsoft Learn module URLs (grounded through the MCP server, never invented), and the lab status for this learner.
