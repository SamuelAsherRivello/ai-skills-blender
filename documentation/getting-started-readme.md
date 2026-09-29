[Back to README.md](../README.md)

# Getting Started

Here are the steps.

### 1. 🛠 Install Blender

1. Install Blender from [blender.org](https://www.blender.org/download/).

### 2. 🛠 Setup Blender MCP

1. Follow the [official Blender MCP setup](https://www.blender.org/lab/mcp-server/) for your AI client.

### 3. 🛠 Install Skills

#### A. Codex

1. Copy the skill folders from [.codex/skills](../.codex/skills/) into `~/.agents/skills/`.

Or run this command from the repository in PowerShell:

```powershell
./scripts/install-codex.ps1 -Scope User -Skills all
```

#### B. Claude

1. Copy the skill folders from [.claude/skills](../.claude/skills/) into `~/.claude/skills/`.

Or run this command from the repository in PowerShell:

```powershell
./scripts/install-claude.ps1 -Scope User -Skills all
```

### 4. 🛠 Test Blender Connection

1. Run `$blender-setup` in Codex or `/blender-setup` in Claude Code.
2. Request a task, such as `Render the current scene.`
