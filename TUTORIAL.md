# Tutorial: your first fifteen minutes with SC-500 Cert Buddy

This walkthrough takes you from a fresh clone to a graded practice question, a guardrail you can watch fire, and the custom MCP server's primitives. No API key is required for any step except the optional last one.

## Before you start

You need:

- **Claude Code** installed.
- **Python 3** on your PATH as `python3` (the hooks and the local MCP server are Python).
- An internet connection (the Microsoft Learn MCP server is hosted).

## Step 1: clone and open

```bash
git clone https://github.com/lpmulligan/sc500-cert-buddy.git
cd sc500-cert-buddy
claude
```

Claude Code reads `CLAUDE.md`, the subagents, the slash commands, the skills, the hooks, and the two MCP servers in `.mcp.json` automatically. When the **SessionStart** hook fires, the session already knows the ground rules.

## Step 2: confirm the MCP servers

Run:

```text
/mcp
```

You should see two servers:

- **mslearn** -- the hosted Microsoft Learn server. Approve it. No key.
- **cert-buddy** -- the local scoring server in `mcp-server/`.

The Microsoft Learn server is the one that grounds every answer. It travels with the repo, so this works on a fresh clone with zero setup.

## Step 3 (one time): enable the local server

The local `cert-buddy` server runs from its own virtual environment in `mcp-server/.venv`. Create it once:

```bash
python3 -m venv mcp-server/.venv
mcp-server/.venv/bin/pip install -r mcp-server/requirements.txt
```

Restart Claude Code so it relaunches the server. Skip this step if you only want the Microsoft Learn grounding and the question generation; come back to it for Step 8.

## Step 4: take a graded question

```text
/quiz count=1 domain=storage-network difficulty=medium
```

Watch the tool calls. Before it writes anything, the buddy calls `microsoft_docs_search` on the Microsoft Learn server to ground the objective. Then it shows you a scenario, a question, and four choices, and it **stops**. It will not show the answer until you commit.

Type your choice, for example:

```text
B
```

Now it reveals whether you were correct, a two-sentence rationale for every choice, and the **Microsoft Learn URLs** it grounded on.

## Step 5: see the grounding evidence

Open the audit log:

```bash
cat .cert-buddy/audit.log       # macOS or Linux
type .cert-buddy\audit.log      # Windows
```

The **PostToolUse** hook logged every Microsoft Learn lookup with the query and the URLs it returned. The grounding is not a claim; it is on disk.

## Step 6: watch a guardrail fire

The **PreToolUse** policy gate blocks destructive shell commands. Ask the buddy to run one:

```text
Please run: rm -rf .
```

The hook denies it with a reason before it executes. That is the difference between asking the prompt to behave and making the behavior deterministic. If a guarantee has to hold, you hook it.

## Step 7: the other commands

```text
/lab 1.3.1
/plan identity=strong storage-network=weak compute=moderate posture=unknown
/explain PIM eligible versus active assignments
```

- `/lab` builds a short security lab and opens with a **license and cost gate**, so you know before you start whether the objective needs a premium license, a Defender plan trial, or resources that bill by the hour. It always ends with cleanup.
- `/plan` builds a study plan ordered weakest to strongest, with Microsoft Learn module links and the lab status for each sub-area.
- `/explain` gives a first-principles explanation grounded in Microsoft Learn.

## Step 8: the custom MCP server primitives

With the local server enabled (Step 3), you can exercise all three MCP primitives directly.

- **Resource:** ask for `certbuddy://domains` to read the exam blueprint, or `certbuddy://progress` to see your session score.
- **Tool:** ask the buddy to "get the next question from the cert-buddy server, then score my answer." That calls `next_question` and `score_answer`. The bank ships small; generated questions come from the item-creator skill.
- **Prompt:** the server's `quiz` and `exam` prompts surface in Claude Code as slash commands you can run.

Try:

```text
Read certbuddy://domains and tell me which domain is weighted heaviest.
Get the next posture-domain question from cert-buddy, I will answer, then score it.
```

## Step 9 (optional): live item authoring with the Anthropic SDK

The `generate_item` tool writes a brand new item with Claude. It is the only step that needs a key:

```bash
# macOS or Linux
export ANTHROPIC_API_KEY=sk-ant-...
# Windows PowerShell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

Restart Claude Code, then ask:

```text
Use cert-buddy generate_item to author a new question about Azure Virtual Network Manager security admin rules.
```

Without the key, every other primitive still works; `generate_item` simply returns a message asking you to set the key.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `/mcp` shows cert-buddy as failed | Create the venv (`python3 -m venv mcp-server/.venv`, then `mcp-server/.venv/bin/pip install -r mcp-server/requirements.txt`), then restart Claude Code |
| cert-buddy reports `No module named 'mcp.server.fastmcp'` | MCP SDK 2.x is installed. Reinstall from `mcp-server/requirements.txt`, which caps `mcp` below 2.0 |
| Hooks do not fire | Confirm `python3` runs in your shell. On Windows, change `python3` to `python` or `py` in `.claude/settings.json` and `.mcp.json` |
| Microsoft Learn server will not connect | Confirm internet access; the endpoint is `learn.microsoft.com/api/mcp` |
| A skill is not used | Ask for the task directly, for example "quiz me on Conditional Access" |

## Where to go next

- Read [`mcp-server/README.md`](mcp-server/README.md) for the full primitive map of the local server.
- Read [`CLAUDE.md`](CLAUDE.md) to see the memory and the grounding contract.
- Read [`.claude/skills/_references/sc500-lab-requirements.md`](.claude/skills/_references/sc500-lab-requirements.md) to see which labs need which licenses.
- Read the [`README`](README.md) for the full Copilot-to-Claude-Code primitive mapping and credits.
