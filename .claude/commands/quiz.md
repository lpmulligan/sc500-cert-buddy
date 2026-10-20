---
description: Run a short SC-500 practice quiz (default 5 questions), one at a time, with progress and an end-of-quiz score. Use count=1 for a single question.
argument-hint: "[count=5] [domain: identity|storage-network|compute|posture] [bloom: Remember|Understand|Apply|Analyze] [difficulty: easy|medium|hard]"
allowed-tools: Read, Grep, Glob, mcp__mslearn__microsoft_docs_search, mcp__mslearn__microsoft_docs_fetch, mcp__mslearn__microsoft_code_sample_search
---

Use the **sc500-cert-buddy** subagent and the **sc500-item-creator** skill to run a short, exam-realistic SC-500 **quiz**.

Requested options (any may be blank): $ARGUMENTS

## How many questions

`count` sets the number of questions. **The default is 5.** Use `count=1` for a single question, up to `count=10`. This is a quiz, so deliver multiple questions by default and do not stop after the first one unless `count=1`.

## If domain, bloom, or difficulty is missing, show the pick-list

When an option is not supplied, show this short menu in plain language, apply sensible defaults to the whole quiz, and say in one line which defaults you used.

**Domain** (which part of the exam):

- `identity` -- Manage identity, access, and governance (20-25%)
- `storage-network` -- Secure storage, databases, and networking (25-30%)
- `compute` -- Secure compute, including security for AI (20-25%)
- `posture` -- Manage and monitor security posture (20-25%)
- *default:* a mix weighted by exam percentage across the quiz

**Bloom level** (how hard you have to think): `Remember`, `Understand`, `Apply` *(default)*, `Analyze`.

**Difficulty:** `easy` | `medium` *(default)* | `hard`.

## Run the quiz, one question at a time

For each question from 1 to `count`:

1. Show progress as a header: **"Question N of {count}"**.
2. Ground the correct behavior in Microsoft Learn through the `mslearn` MCP server.
3. **Phase 1:** present the metadata, the scenario stem, and the four answer choices ONLY. Then stop and wait for my answer (a letter, or `hint`, or `skip`).
4. **Phase 2:** after I answer, reveal the correct letter, a two-sentence rationale per choice, and the Microsoft Learn URLs. Keep a running tally, then continue to the next question.

Randomize the correct letter across A, B, C, and D, and the fictional company across the approved list, on every question. Do not repeat an objective within the same quiz.

## End-of-quiz summary

After the final question, show a summary:

- **Score: X of {count} correct**, plus the percentage.
- A per-domain breakdown (identity, storage-network, compute, posture).
- The two or three objectives to review next, each with a Microsoft Learn link, based on what I missed.
- One short, encouraging line on where to focus.
