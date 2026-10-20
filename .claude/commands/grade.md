---
description: Grade a lab submission against its canonical answer key using the cert-buddy MCP server.
argument-hint: "[lab slug] (the folder name under labs/)"
allowed-tools: Read, mcp__cert-buddy__grade_lab
---

Grade the lab named: $ARGUMENTS

1. Read `labs/<slug>/answer-key.json` (the canonical key) and `labs/<slug>/submission.json` (the learner's recorded results). If the submission file is missing, explain its shape: a JSON object that maps each check `id` from the answer key to the value the learner observed, for example `{ "jit_policy_created": "yes", "nsg_rule_source": "203.0.113.10" }`. A learner who followed the no-license path adds `"_path": "no-license"`.
2. Call the **cert-buddy** MCP tool `grade_lab` with the answer key and the submission.
3. Report the earned points, the percentage, and a per-check pass or fail list. If the learner followed the no-license path, say which checks were left out of the score because they need a license. For any miss, show the expected value next to the submitted value, and point back to the Microsoft Learn references in the lab so the learner can close the gap. Keep the tone encouraging.
