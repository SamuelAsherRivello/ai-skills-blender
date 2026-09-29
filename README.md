# Blender Skills for Codex and Claude Code

Thirteen focused skills for the official Blender Lab MCP connection. Shared sources live in [skills/](skills/), with client packages in [.codex/](.codex/INSTALL.md) and [.claude/](.claude/INSTALL.md).

## Images

### Screenshots

Reference sheets from the optional gallery (inspiration, not generated project output):

<a href="references/renders/render_architecture_v1.png"><img src="references/renders/render_architecture_v1.png" width="400" alt="Architectural render reference sheet" /></a>
<a href="references/renders/render_character_v1.png"><img src="references/renders/render_character_v1.png" width="400" alt="Character render reference sheet" /></a>

[Visual references](references/) contains the original 20 PNGs in camera, colors, lighting and renders. Textual styles remain usable without the optional gallery.

## Live Demo

These skills run locally in Codex with Blender. There is no hosted demo. See the [live Blender acceptance results](docs/acceptance.md) and [validation instructions](docs/helpers.md#maintainer-validation).

## Table of Contents

1. [Images](#images)
2. [Live Demo](#live-demo)
3. [Getting Started](#getting-started)
4. [Project Details](#project-details)
5. [Credits](#credits)

## Getting Started

Here are the steps.

### 1. 🛠 Install Blender

1. Install Blender from [blender.org](https://www.blender.org/download/).

### 2. 🛠 Setup Blender MCP

1. Follow the [official Blender MCP setup](https://www.blender.org/lab/mcp-server/) for your AI client.

### 3. 🛠 Install Skills

1. **For Codex:** Copy the skill folders from [.codex/skills](.codex/skills/) into `~/.agents/skills/`.
2. **For Claude Code:** Copy the skill folders from [.claude/skills](.claude/skills/) into `~/.claude/skills/`.

Or run this command from the repository in PowerShell:

```powershell
# For Codex
./scripts/install-codex.ps1 -Scope User -Skills all

# For Claude Code
./scripts/install-claude.ps1 -Scope User -Skills all
```

### 4. 🛠 Use Skills

1. Run `$blender-setup` in Codex or `/blender-setup` in Claude Code.
2. Request a task, such as `Render the current scene.`

## Project Details

Windows/Codex has live Blender validation. Claude packaging and installation are tested; a full Claude session is not yet verified. Other platforms are not yet verified. Source content remains portable and avoids personal configuration paths.

### 📝 Structure

- skills/: shared authoring sources for thirteen skills.
- .codex/skills/: generated Codex package with OpenAI metadata.
- .claude/skills/: generated Claude package with a client-specific setup workflow.
- scripts/: installation and development validation tools.
- references/: the original camera, colors, lighting and renders directories.
- docs/: input guidance, helper interfaces, source provenance and validation evidence.

Local tests, OpenSpec planning, generated acceptance outputs, environments and caches are excluded from Git. Intentional future PNG references and Blender source assets are not blanket-ignored.

### 📦 AI

Both clients use `SKILL.md` and supporting resources. The Codex package also includes `agents/openai.yaml`; the Claude package adapts setup to Claude MCP and omits Codex-only metadata. Run `python scripts/sync-client-skills.py` after editing shared sources, and `python scripts/sync-client-skills.py --check` to verify the mirrors. Supporting resources stay with their owning skill so individual installation works.

The optional shared gallery is loaded only when useful. Select a reference by filename and inspect the image before applying its visual characteristics. See [input conventions](docs/inputs.md) and [helper interfaces](docs/helpers.md).

Claude uses `/skill-name` for the same catalog shown below with Codex `$skill-name` syntax.

#### Skill Catalog

| Command | Purpose |
|---|---|
| `$blender-setup` | Read-only chronological connection diagnosis |
| `$blender-create-model` | Model a scoped prop or character |
| `$blender-create-environment` | Build modular Blender environments |
| `$blender-procedural-geometry` | Create reproducible Blender geometry |
| `$blender-materials` | Create and inspect Blender materials |
| `$blender-uv-bake` | Unwrap meshes and verify baked maps |
| `$blender-light-camera` | Compose cameras and shape lighting |
| `$blender-render` | Render and verify Blender outputs |
| `$blender-rig-animate` | Rig assets and review animation |
| `$blender-game-export` | Export Blender assets for game engines |
| `$blender-review-optimize` | Audit and optimize Blender scenes |
| `$blender-convert-3d-2d` | Convert Blender models into 2D sprites |
| `$blender-convert-2d-3d` | Reconstruct Blender models from images |

### 📦 Dependencies

- [Blender](https://www.blender.org/)
- [Official Blender Lab MCP](https://www.blender.org/lab/mcp-server/)
- AI Harness (e.g. Codex)

## Credits

<!-- AI: Preserve established attribution and ownership. Customize the following subsections only from confirmed contributor, contact, and license information; do not infer a new owner from the repository name. -->
### 💡 Contributors

<!-- AI: Preserve existing contributor credit and add contributors only when confirmed. Do not automatically advance experience counts or their reference year. -->
- Samuel Asher Rivello - Over 25 years of game development XP (2026)

### 💡 Contact

<!-- AI: Preserve confirmed contact destinations and their order unless requested otherwise. Use readable display URLs without a protocol or trailing slash while keeping the real link target intact. Do not invent accounts or change target capitalization based on display styling. -->
- [LinkedIn.com/in/SamuelAsherRivello](https://Linkedin.com/in/SamuelAsherRivello) ⭐ 
- [GitHub.com/SamuelAsherRivello](https://github.com/SamuelAsherRivello/)
- [Twitter.com/srivello](https://twitter.com/srivello/)
- Resume / Portfolio: [SamuelAsherRivello.com](http://www.SamuelAsherRivello.com)


### 💡 License

<!-- AI: Keep the license name linked to the actual relative license file and verify that its terms match this statement. Keep the copyright holder and year consistent with that file. Do not change license terms, ownership, or dates without an explicit request. -->
- Provided as-is under the [MIT License](LICENSE).

- Copyright © 2026 Rivello Multimedia Consulting, LLC.
