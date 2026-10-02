[Back to README.md](../README.md)

# Getting Started

## 1. Get the skills

From your project directory, run:

```sh
npx skills@latest add SamuelAsherRivello/ai-skills-blender --copy
```

Choose the Blender skills you want and the agents to install them for, including Codex and Claude Code. Project-local installation is the recommended default. `--copy` installs ordinary files you can edit.

To install globally instead, add `--global`:

```sh
npx skills@latest add SamuelAsherRivello/ai-skills-blender --copy --global
```

The existing [Codex](../.codex/INSTALL.md) and [Claude Code](../.claude/INSTALL.md) PowerShell installers remain available for package-specific installation.

## 2. Update the skills

For project-local installations:

```sh
npx skills update --project
```

For global installations:

```sh
npx skills update --global
```

## 3. Set up Blender MCP

1. Install Blender from [blender.org](https://www.blender.org/download/).
2. Follow the [official Blender MCP setup](https://www.blender.org/lab/mcp-server/) for your AI client.

## 4. Test the Blender connection

1. Run `$blender-setup` in Codex or `/blender-setup` in Claude Code.
2. Request a task, such as `Render the current scene.`
