# Installing Blender Skills for Claude Code

## Prerequisites

Claude Code, Blender and the [official Blender Lab MCP connection](https://www.blender.org/lab/mcp-server/) configured in Claude. A Codex MCP registration alone does not configure Claude.

## Installation

This checkout already contains native project skills in .claude/skills/. Open Claude Code in the repository to use them after accepting the normal workspace trust prompt.

To copy skills into your user scope or another project, run from this repository in PowerShell:

```powershell
./scripts/install-claude.ps1 -Scope User -Skills all
```

For a project use -Scope Project -ProjectPath C:\MyProject. Add -DryRun to preview. Existing destinations require explicit -Replace and receive recoverable backups. No MCP configuration is installed.

## Verify

Invoke /blender-setup, then /blender-render Render the current scene.

Packaging, resources and temporary-destination installation are tested. Live Blender execution was verified through Codex; a full Claude Code session has not yet been verified. Claude's setup adapter uses its own /mcp status and live tools, not Codex configuration.

## Updating

Pull this repository. For copied installations, rerun the installer with -Replace. Shared content lives in skills/; the Claude setup adapter lives in scripts/adapters/. Run python scripts/sync-client-skills.py after authoring changes.

Claude uses the same SKILL.md frontmatter and supporting files. Codex-only agents/openai.yaml files are omitted from this package.

## Windows execution

No auxiliary command windows are permitted, including brief flashes. Agents must use existing MCP tools when available and establish windowless behavior before launching helpers or the commands shown in this document. A visible terminal is not a fallback. If the outer client launch or a descendant is unverified, report that operation as blocked and continue safe work.

The setup helper includes a captured, bounded windowless runner with owned-process cleanup. Its SDK fallback probe currently blocks: the inspected MCP SDK 1.30.0 retries without console suppression. Use native session MCP tools for live connectivity. Executable resolution (including absolute paths and cmd /c) is separate from console suppression; Blender --background and hidden-window styling alone do not prove absence of flashes. Keep the existing Blender editor state unchanged.