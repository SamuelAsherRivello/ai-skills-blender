# Installing Blender Skills for Codex

## Prerequisites

Local Codex, Blender and the [official Blender Lab MCP connection](https://www.blender.org/lab/mcp-server/).

## Installation

From this repository in PowerShell, preview a project-local install and then install:

```powershell
./scripts/install-codex.ps1 -Scope Project -ProjectPath C:\MyProject -Skills all -DryRun
./scripts/install-codex.ps1 -Scope Project -ProjectPath C:\MyProject -Skills all
```

Use `-Scope User` to make skills available across projects. Select individual names with `-Skills`; the installer also includes any sibling skill whose linked resources are required. Existing destinations require explicit `-Replace` and receive recoverable backups.

The repository package is .codex/skills/. Codex's current discovery destination is .agents/skills/ in the chosen project or user home. Keeping a distribution copy under .codex does not replace that installation step.

On other platforms, copy selected folders from `.codex/skills/` into the destination project's `.agents/skills/`. A repository-wide `npx skills add` scans both shared and client package directories and cannot currently guarantee which same-name variant it chooses. Use this package when the Codex setup workflow matters.

## Verify

Restart Codex if necessary, then invoke $blender-setup. Setup and Blender workflows have been exercised in local Codex on Windows.

## Updating

Pull this repository and rerun the installer with `-Replace` when ready to replace an installed copy. The Codex package is curated in `.codex/skills/` and validated separately from `skills/`; `scripts/sync-client-skills.py` updates only the Claude package. Keep corresponding shared and Codex guidance consistent when a change applies to both.

## Windows execution

Agents must create no auxiliary command windows, including brief flashes. Use existing MCP tools where possible. Before running any command above, establish windowless behavior for its outer launcher and descendants; otherwise report BLOCKED and do not launch. Never retry in a visible terminal. The setup helper's SDK fallback currently blocks because the inspected MCP SDK 1.30.0 can retry without console suppression. Use native session tools for live checks. Preserve the existing Blender editor state.
