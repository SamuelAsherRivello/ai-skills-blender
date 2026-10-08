[Back to README.md](../README.md)

# Getting Started

## 1. Get the skills

Clone this repository. On Windows, run the matching installer from the repository root. For Codex:

```powershell
./scripts/install-codex.ps1 -Scope Project -ProjectPath C:\MyProject -Skills all -DryRun
./scripts/install-codex.ps1 -Scope Project -ProjectPath C:\MyProject -Skills all
```

For Claude Code, use the checked-in [Claude package](../.claude/INSTALL.md):

```powershell
./scripts/install-claude.ps1 -Scope Project -ProjectPath C:\MyProject -Skills all -DryRun
./scripts/install-claude.ps1 -Scope Project -ProjectPath C:\MyProject -Skills all
```

On other platforms, copy selected folders from `.codex/skills/` to the destination project's `.agents/skills/` for Codex, or from `.claude/skills/` to `.claude/skills/` for Claude Code. This package contains a Claude-specific `blender-setup` adapter. A repository-wide `npx skills add` currently deduplicates same-name client variants, so it cannot guarantee which setup variant is installed. Do not install duplicate copies under the same client.

## 2. Update the skills

Pull this repository and copy the selected package folders again. The Windows installers require `-Replace` for existing destinations and save backups. To maintain or retheme this repository, see the [adaptation guide](adapting-repository.md).

## 3. Set up Blender MCP

1. Install Blender from [blender.org](https://www.blender.org/download/).
2. Follow the [official Blender MCP setup](https://www.blender.org/lab/mcp-server/) for your AI client.

## 4. Test the Blender connection

1. Run `$blender-setup` in Codex or `/blender-setup` in Claude Code.
2. Request a task, such as `Render the current scene.`
