# Build the installable Claude Code plugin from the project primitives.
#
# Single source of truth is .claude/ and mcp-server/. This script copies those
# into plugin/sc500-cert-buddy/ in the layout Claude Code plugins expect, and
# writes the plugin-scoped .mcp.json and hooks/hooks.json. Re-run it after you
# edit any agent, command, skill, hook, or the MCP server, then commit.
#
# Usage:  pwsh ./scripts/build-plugin.ps1
$ErrorActionPreference = 'Stop'
$root   = Split-Path -Parent $PSScriptRoot
$plugin = Join-Path $root 'plugin\sc500-cert-buddy'

Write-Host "Building plugin into $plugin"

# Clean the generated component folders (the manifest and README are kept).
foreach ($d in 'agents', 'commands', 'skills', 'hooks', 'mcp-server') {
    $p = Join-Path $plugin $d
    if (Test-Path $p) { Remove-Item -Recurse -Force $p }
}
New-Item -ItemType Directory -Force -Path $plugin | Out-Null

# Copy the primitives from the project.
Copy-Item (Join-Path $root '.claude\agents')   (Join-Path $plugin 'agents')   -Recurse -Force
Copy-Item (Join-Path $root '.claude\commands') (Join-Path $plugin 'commands') -Recurse -Force
Copy-Item (Join-Path $root '.claude\skills')   (Join-Path $plugin 'skills')   -Recurse -Force
Copy-Item (Join-Path $root '.claude\hooks')    (Join-Path $plugin 'hooks')    -Recurse -Force

# Bundle the FastMCP server, minus local build artifacts.
Copy-Item (Join-Path $root 'mcp-server') (Join-Path $plugin 'mcp-server') -Recurse -Force
foreach ($junk in '.venv', '__pycache__', 'data\__pycache__') {
    $j = Join-Path $plugin "mcp-server\$junk"
    if (Test-Path $j) { Remove-Item -Recurse -Force $j }
}

# Plugin-scoped MCP config. ${CLAUDE_PLUGIN_ROOT} resolves to the plugin folder.
$mcp = @'
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
'@
Set-Content -Encoding ascii (Join-Path $plugin '.mcp.json') $mcp

# Plugin hooks, same shape as .claude/settings.json but rooted at the plugin.
$hooks = @'
{
  "hooks": {
    "SessionStart": [ { "hooks": [ { "type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/session-start.py\"" } ] } ],
    "UserPromptSubmit": [ { "hooks": [ { "type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/prompt-context.py\"" } ] } ],
    "PreToolUse": [ { "matcher": "Bash", "hooks": [ { "type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/policy-gate.py\"" } ] } ],
    "PostToolUse": [ { "matcher": "mcp__mslearn__.*", "hooks": [ { "type": "command", "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/citation-audit.py\"" } ] } ]
  }
}
'@
Set-Content -Encoding ascii (Join-Path $plugin 'hooks\hooks.json') $hooks

Write-Host "Plugin build complete."
