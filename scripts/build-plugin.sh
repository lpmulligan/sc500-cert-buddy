#!/usr/bin/env bash
# Build the installable Claude Code plugin from the project primitives.
#
# Single source of truth is .claude/ and mcp-server/. Re-run after edits, then commit.
# Usage:  ./scripts/build-plugin.sh
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
plugin="$root/plugin/sc500-cert-buddy"

echo "Building plugin into $plugin"
for d in agents commands skills hooks mcp-server; do
  rm -rf "$plugin/$d"
done
mkdir -p "$plugin"

cp -r "$root/.claude/agents"   "$plugin/agents"
cp -r "$root/.claude/commands" "$plugin/commands"
cp -r "$root/.claude/skills"   "$plugin/skills"
cp -r "$root/.claude/hooks"    "$plugin/hooks"
cp -r "$root/mcp-server"       "$plugin/mcp-server"
rm -rf "$plugin/mcp-server/.venv" "$plugin/mcp-server/__pycache__" "$plugin/mcp-server/data/__pycache__"

cat > "$plugin/.mcp.json" <<'JSON'
{
  "mcpServers": {
    "mslearn": { "type": "http", "url": "https://learn.microsoft.com/api/mcp" },
    "cert-buddy": {
      "type": "stdio",
      "command": "python3",
      "args": ["${CLAUDE_PLUGIN_ROOT}/mcp-server/cert_buddy_mcp.py"]
    }
  }
}
JSON

cat > "$plugin/hooks/hooks.json" <<'JSON'
{
  "hooks": {
    "SessionStart": [ { "hooks": [ { "type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/session-start.py\"" } ] } ],
    "UserPromptSubmit": [ { "hooks": [ { "type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/prompt-context.py\"" } ] } ],
    "PreToolUse": [ { "matcher": "Bash", "hooks": [ { "type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/policy-gate.py\"" } ] } ],
    "PostToolUse": [ { "matcher": "mcp__mslearn__.*", "hooks": [ { "type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/citation-audit.py\"" } ] } ]
  }
}
JSON

echo "Plugin build complete."
