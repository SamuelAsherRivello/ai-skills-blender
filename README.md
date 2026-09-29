<p>
<img src="https://raw.githubusercontent.com/SamuelAsherRivello/github-repository-template/main/project-name/documentation/samuel-asher-rivello-banner.png" alt="Samuel Asher Rivello" width="100%" /><br />
<img src="docs/images/youtube-thumbnail.png" alt="Blender AI skills YouTube thumbnail" width="100%" />
</p>

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-13-orange.svg)](skills/)
[![Blender MCP](https://img.shields.io/badge/Blender_MCP-official-blueviolet.svg)](https://www.blender.org/lab/mcp-server/)
[![Codex](https://img.shields.io/badge/Codex-skills-green.svg)](.codex/INSTALL.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-skills-black.svg)](.claude/INSTALL.md)

# Blender Skills for Codex and Claude Code

Create, refine, and render 3D assets with thirteen reusable Blender skills.<br />
Shared sources live in [skills/](skills/), with client packages in [.codex/](.codex/INSTALL.md) and [.claude/](.claude/INSTALL.md).

> [!IMPORTANT]
> Skills designed to work with the existing [official Blender Lab MCP](https://www.blender.org/lab/mcp-server/).

## Images

### Screenshots

Reference sheets from the optional gallery (inspiration, not generated project output):

<a href="references/renders/render_architecture_v1.png"><img src="references/renders/render_architecture_v1.png" width="400" alt="Architectural render reference sheet" /></a>
<a href="references/renders/render_character_v1.png"><img src="references/renders/render_character_v1.png" width="400" alt="Character render reference sheet" /></a>

[Visual references](references/) contains the original 20 PNGs in camera, colors, lighting and renders. Textual styles remain usable without the optional gallery.

## Live Demo

Coming Soon...

## Table of Contents

1. [Getting Started](#getting-started)
2. [Use Skills](#use-skills)
3. [Project Details](#project-details)
4. [Credits](#credits)

## Getting Started

Here are the steps.

### 1. 🛠 Install Blender

1. Install Blender from [blender.org](https://www.blender.org/download/).

### 2. 🛠 Setup Blender MCP

1. Follow the [official Blender MCP setup](https://www.blender.org/lab/mcp-server/) for your AI client.

### 3. 🛠 Install Skills

#### A. Codex

1. Copy the skill folders from [.codex/skills](.codex/skills/) into `~/.agents/skills/`.

Or run this command from the repository in PowerShell:

```powershell
./scripts/install-codex.ps1 -Scope User -Skills all
```

#### B. Claude

1. Copy the skill folders from [.claude/skills](.claude/skills/) into `~/.claude/skills/`.

Or run this command from the repository in PowerShell:

```powershell
./scripts/install-claude.ps1 -Scope User -Skills all
```

### 4. 🛠 Test Blender Connection

1. Run `$blender-setup` in Codex or `/blender-setup` in Claude Code.
2. Request a task, such as `Render the current scene.`

## Use Skills

Claude uses `/skill-name` for the same catalog shown below with Codex `$skill-name` syntax.

### Calling a skill with reference

```text
$blender-create-model
Subject: A boy getting ready for school, putting on a backpack.
Render style: Comic book; use references/renders/render_character_v1.png as inspiration.
Lighting: Warm morning light; consult references/lighting/lighting_character_v1.png.
Setting: A cozy bedroom with school supplies.
Camera: Full-body, three-quarter view at the character's eye level.
Colors: Muted blues with yellow accents.
Output: Editable Blender scene and a 1920x1080 PNG preview.
Inspect the referenced images and choose treatments that fit this brief.
```

For Claude, replace `$blender-create-model` with `/blender-create-model`. Use absolute image paths if the reference folder is outside your current project.

## Skills

| Name | Comment | Call Directly? |
|---|---|---|
| `$blender-setup` | Check the Blender connection and diagnose setup issues | ![Yes](https://img.shields.io/badge/Yes-2ea44f?style=flat) |
| `$blender-create-model` | Create a prop or character | ![Yes](https://img.shields.io/badge/Yes-2ea44f?style=flat) |
| `$blender-create-environment` | Build a room, landscape, or modular scene | ![Yes](https://img.shields.io/badge/Yes-2ea44f?style=flat) |
| `$blender-procedural-geometry` | Build editable generators and repeated geometry | ![Optional](https://img.shields.io/badge/Optional-f2cc60?style=flat) |
| `$blender-materials` | Create or refine surface materials | ![Optional](https://img.shields.io/badge/Optional-f2cc60?style=flat) |
| `$blender-uv-bake` | Unwrap meshes and bake texture maps | ![Optional](https://img.shields.io/badge/Optional-f2cc60?style=flat) |
| `$blender-light-camera` | Refine lighting and camera composition | ![Optional](https://img.shields.io/badge/Optional-f2cc60?style=flat) |
| `$blender-render` | Render the current scene and verify outputs | ![Yes](https://img.shields.io/badge/Yes-2ea44f?style=flat) |
| `$blender-rig-animate` | Rig an asset or create animation clips | ![Yes](https://img.shields.io/badge/Yes-2ea44f?style=flat) |
| `$blender-game-export` | Export an asset for a game engine | ![Yes](https://img.shields.io/badge/Yes-2ea44f?style=flat) |
| `$blender-review-optimize` | Review asset quality and reduce rendering or geometry cost | ![Optional](https://img.shields.io/badge/Optional-f2cc60?style=flat) |
| `$blender-convert-3d-2d` | Render a model into sprites or other 2D views | ![Yes](https://img.shields.io/badge/Yes-2ea44f?style=flat) |
| `$blender-convert-2d-3d` | Reconstruct a model from an image | ![Yes](https://img.shields.io/badge/Yes-2ea44f?style=flat) |

**Yes** marks a common starting point. **Optional** marks a specialist task that can also support a larger workflow. All skills can be called directly; these labels are guidance, not invocation restrictions. The AI can select relevant installed skills, but there is no fixed automatic chain between them.

## Reference

Click a thumbnail to open the full-size image.

| Name | Image |
|---|---|
| Camera Angles V1 | <a href="references/camera/camera_angles_v1.png"><img src="references/camera/camera_angles_v1.png" width="50" height="50" alt="Camera Angles V1" /></a> |
| Colors Hand V1 | <a href="references/colors/colors_hand_v1.png"><img src="references/colors/colors_hand_v1.png" width="50" height="50" alt="Colors Hand V1" /></a> |
| Colors Leaves V1 | <a href="references/colors/colors_leaves_v1.png"><img src="references/colors/colors_leaves_v1.png" width="50" height="50" alt="Colors Leaves V1" /></a> |
| Lighting Character V1 | <a href="references/lighting/lighting_character_v1.png"><img src="references/lighting/lighting_character_v1.png" width="50" height="50" alt="Lighting Character V1" /></a> |
| Render Architecture V1 | <a href="references/renders/render_architecture_v1.png"><img src="references/renders/render_architecture_v1.png" width="50" height="50" alt="Render Architecture V1" /></a> |
| Render Car V1 | <a href="references/renders/render_car_v1.png"><img src="references/renders/render_car_v1.png" width="50" height="50" alt="Render Car V1" /></a> |
| Render Character V1 | <a href="references/renders/render_character_v1.png"><img src="references/renders/render_character_v1.png" width="50" height="50" alt="Render Character V1" /></a> |
| Render Character V2 | <a href="references/renders/render_character_v2.png"><img src="references/renders/render_character_v2.png" width="50" height="50" alt="Render Character V2" /></a> |
| Render Desk Lamp V1 | <a href="references/renders/render_desk_lamp_v1.png"><img src="references/renders/render_desk_lamp_v1.png" width="50" height="50" alt="Render Desk Lamp V1" /></a> |
| Render Desk Lamp V2 | <a href="references/renders/render_desk_lamp_v2.png"><img src="references/renders/render_desk_lamp_v2.png" width="50" height="50" alt="Render Desk Lamp V2" /></a> |
| Render Food V1 | <a href="references/renders/render_food_v1.png"><img src="references/renders/render_food_v1.png" width="50" height="50" alt="Render Food V1" /></a> |
| Render Food V2 | <a href="references/renders/render_food_v2.png"><img src="references/renders/render_food_v2.png" width="50" height="50" alt="Render Food V2" /></a> |
| Render Forest V1 | <a href="references/renders/render_forest_v1.png"><img src="references/renders/render_forest_v1.png" width="50" height="50" alt="Render Forest V1" /></a> |
| Render Fox V1 | <a href="references/renders/render_fox_v1.png"><img src="references/renders/render_fox_v1.png" width="50" height="50" alt="Render Fox V1" /></a> |
| Render Fox V2 | <a href="references/renders/render_fox_v2.png"><img src="references/renders/render_fox_v2.png" width="50" height="50" alt="Render Fox V2" /></a> |
| Render Interior V1 | <a href="references/renders/render_interior_v1.png"><img src="references/renders/render_interior_v1.png" width="50" height="50" alt="Render Interior V1" /></a> |
| Render Landscape V1 | <a href="references/renders/render_landscape_v1.png"><img src="references/renders/render_landscape_v1.png" width="50" height="50" alt="Render Landscape V1" /></a> |
| Render Robot V1 | <a href="references/renders/render_robot_v1.png"><img src="references/renders/render_robot_v1.png" width="50" height="50" alt="Render Robot V1" /></a> |
| Render Sword V1 | <a href="references/renders/render_sword_v1.png"><img src="references/renders/render_sword_v1.png" width="50" height="50" alt="Render Sword V1" /></a> |
| Render Treasure Chest V1 | <a href="references/renders/render_treasure_chest_v1.png"><img src="references/renders/render_treasure_chest_v1.png" width="50" height="50" alt="Render Treasure Chest V1" /></a> |

## Project Details

Windows/Codex has live Blender validation. Claude packaging and installation are tested; a full Claude session is not yet verified. Other platforms are not yet verified. Source content remains portable and avoids personal configuration paths.

### 📝 Structure

- `skills/`: shared authoring sources for thirteen skills.
- `.codex/skills/`: generated Codex package with OpenAI metadata.
- `.claude/skills/`: generated Claude package with a client-specific setup workflow.
- `scripts/`: installation and development validation tools.
- `references/`: the original camera, colors, lighting and renders directories.
- `docs/`: input guidance, helper interfaces, source provenance and validation evidence.

Local tests, OpenSpec planning, generated acceptance outputs, environments and caches are excluded from Git. Intentional future PNG references and Blender source assets are not blanket-ignored.

### 📦 AI

Both clients use `SKILL.md` and supporting resources. The Codex package also includes `agents/openai.yaml`; the Claude package adapts setup to Claude MCP and omits Codex-only metadata. Run `python scripts/sync-client-skills.py` after editing shared sources, and `python scripts/sync-client-skills.py --check` to verify the mirrors. Supporting resources stay with their owning skill so individual installation works.

The optional shared gallery is loaded only when useful. Select a reference by filename and inspect the image before applying its visual characteristics. See [input conventions](docs/inputs.md) and [helper interfaces](docs/helpers.md).

### 📦 Dependencies

- [Blender](https://www.blender.org/)
- [Official Blender Lab MCP](https://www.blender.org/lab/mcp-server/)
- AI Harness: Ex. [Codex](https://openai.com/codex/), [Claude](https://claude.ai/)

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
