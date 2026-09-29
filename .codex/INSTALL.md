# Installing Blender Skills for Codex

## Prerequisites

Local Codex, Blender and the [official Blender Lab MCP connection](https://www.blender.org/lab/mcp-server/).

## Installation

From this repository in PowerShell:

```powershell
./scripts/install-codex.ps1 -Scope User -Skills all
```

For a project, use -Scope Project -ProjectPath C:\MyProject. Add -DryRun to preview. Existing destinations require explicit -Replace and receive recoverable backups.

The repository package is .codex/skills/. Codex's current discovery destination is .agents/skills/ in the chosen project or user home. Keeping a distribution copy under .codex does not replace that installation step.

## Verify

Restart Codex if necessary, then invoke $blender-setup. Setup and Blender workflows have been exercised in local Codex on Windows.

## Updating

Pull this repository and rerun the installer with -Replace when ready to replace an installed copy. Author shared changes in skills/, then run python scripts/sync-client-skills.py. Do not hand-edit generated mirrors.
