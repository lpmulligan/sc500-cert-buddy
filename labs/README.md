# Labs and grading

Each lab the buddy generates is saved here as its own folder, `labs/<slug>/`, so it can be auto-graded against a canonical answer key.

## Files in a lab folder

| File | Who writes it | Purpose |
| --- | --- | --- |
| `lab.md` | the buddy (`/lab`) | The learner-facing hands-on lab: objective, steps, validation gates, cleanup |
| `answer-key.json` | the buddy (`/lab`) | The canonical key a grader compares against |
| `submission.json` | the learner | What the learner actually observed, keyed by check `id` |

## answer-key.json schema

```json
{
  "lab_id": "3-2-3-jit-vm-access",
  "objective": "3.2.3 Enable and enforce use of just-in-time (JIT) VM access",
  "domain": "compute",
  "total_points": 100,
  "checks": [
    { "id": "plan2_enabled",     "description": "Defender for Servers Plan 2 is on for Sub1",          "expected": "yes",          "points": 20, "requires_license": true },
    { "id": "jit_policy_ports",  "description": "The JIT policy on VM1 covers this port",              "expected": "3389",         "points": 30, "requires_license": true },
    { "id": "nsg_default_rule",  "description": "Action of the NSG rule JIT manages when no request is active", "expected": "Deny", "points": 30 },
    { "id": "cleanup_done",      "description": "RG1 was deleted and the plan was turned off",          "expected": "yes",          "points": 20 }
  ]
}
```

Each check has an `id` (stable key), a `description`, an `expected` value, and `points`. The sum of `points` should equal `total_points`. Set `"requires_license": true` on any check that the lab's no-license path cannot complete.

## submission.json shape

A flat object mapping each check `id` to the value the learner observed:

```json
{
  "plan2_enabled": "yes",
  "jit_policy_ports": "3389",
  "nsg_default_rule": "Deny",
  "cleanup_done": "no"
}
```

## The no-license path

Labs for objectives that need a premium license or paid plan include a read-only no-license path. A learner who follows it adds one key to the submission:

```json
{
  "_path": "no-license",
  "nsg_default_rule": "Deny",
  "cleanup_done": "yes"
}
```

The grader then leaves every check marked `requires_license` out of the score, including out of `total_points`, and lists the skipped checks in `skipped_requires_license`.

## Grading

Run `/grade <slug>`. The command reads `answer-key.json` and `submission.json` and calls the **cert-buddy** MCP tool `grade_lab`, which compares each submitted value against the expected value (case-insensitive, trimmed), sums the points for passing checks, and returns the score, the percentage, and a per-check pass or fail list. Comparison is intentionally simple and transparent so the grading is easy to audit and extend.
