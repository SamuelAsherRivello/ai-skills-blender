<p>
<img src="https://raw.githubusercontent.com/SamuelAsherRivello/github-repository-template/main/project-name/documentation/samuel-asher-rivello-banner.png" alt="Samuel Asher Rivello" width="600" /><br /><br />
  
<img src="documentation/marketing/images/youtube-thumbnail.png" alt="Blender AI skills YouTube thumbnail" width="600" />
</p>

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Blender MCP](https://img.shields.io/badge/Blender_MCP-official-blueviolet.svg)](https://www.blender.org/lab/mcp-server/)
[![Codex](https://img.shields.io/badge/Codex-skills-green.svg)](.codex/INSTALL.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-skills-black.svg)](.claude/INSTALL.md)

# AI Skills Blender

Create, refine, and render 3D assets with reusable Blender skills.<br />
Shared skill sources live in [skills/](skills/). The [Codex package](.codex/INSTALL.md) is curated separately; the [Claude package](.claude/INSTALL.md) is generated from the shared sources with a Claude-specific setup adapter.

> [!IMPORTANT]
> Skills designed to work with the existing [official Blender Lab MCP](https://www.blender.org/lab/mcp-server/).

## Images

### Example

| From Sketch | | To 3D Blender Scene |
|:---:|:---:|:---:|
| <a href="documentation/examples/11-floating-forest-from-sketch/input/sketch.png"><img src="documentation/examples/11-floating-forest-from-sketch/input/sketch.png" height="240" alt="Original pencil sketch of a floating forest island" /></a> | <img src="documentation/marketing/images/sketch-to-scene-arrow.svg" width="48" height="48" alt="→" /> | <a href="documentation/examples/11-floating-forest-from-sketch/output/result.png"><img src="documentation/examples/11-floating-forest-from-sketch/output/result.png" height="240" alt="Floating forest reconstructed and rendered in Blender" /></a> |

## Live Demo

- See Live Demo on Readme: [Model Viewer](https://github.com/SamuelAsherRivello/ai-skills-blender-model-viewer#live-demo)

## Table of Contents

1. [Getting Started](#getting-started)
2. [Use Skills](#use-skills)
3. [Project Details](#project-details)
4. [Contributions](#contributions)
5. [Credits](#credits)

## Getting Started

### 1. Choose your AI client

| Client | Recommended installation | Setup check |
|---|---|---|
| Codex | Copy the [Codex package](.codex/INSTALL.md) | `$blender-setup` |
| Claude Code | Copy the [Claude package](.claude/INSTALL.md), which has a Claude-specific setup skill | `/blender-setup` |
| Other agents | Adapt the shared skills and setup instructions to that client's MCP commands | Use that client's skill invocation |

On Windows, clone this repository, then run the relevant installer from its root. Preview the destination first:

```powershell
./scripts/install-codex.ps1 -Scope Project -ProjectPath C:\MyProject -Skills all -DryRun
./scripts/install-codex.ps1 -Scope Project -ProjectPath C:\MyProject -Skills all
```

For Claude Code, use the same flow with its installer:

```powershell
./scripts/install-claude.ps1 -Scope Project -ProjectPath C:\MyProject -Skills all -DryRun
./scripts/install-claude.ps1 -Scope Project -ProjectPath C:\MyProject -Skills all
```

On other platforms, copy the selected folders from `.codex/skills/` into the destination project's `.agents/skills/` for Codex, or from `.claude/skills/` into `.claude/skills/` for Claude Code. The Claude package contains a different `blender-setup` skill. The [`skills` CLI discovers both shared and client package folders](https://github.com/vercel-labs/skills#skill-discovery) and [currently deduplicates same-name variants](https://github.com/vercel-labs/skills/issues/1290), so a repository-wide `npx skills add` cannot guarantee the intended client variant. Do not install the same skill twice through different routes.

### 2. Update the skills

Pull this repository and copy the selected package folders again. On Windows, rerun the matching installer with `-Replace` to keep recoverable backups. Before using the skills, install Blender and configure the official Blender MCP connection **in the AI client you use**. See the [getting started guide](documentation/getting-started-readme.md).

## Use Skills

Codex uses `$skill-name`; Claude Code uses `/skill-name`. Other agents may invoke installed skills by name or discover them from a matching request.

### Calling a skill

```text
$blender-create-model A boy getting ready for school, putting on a backpack.
```

### Calling a skill with reference arguments

```text
$blender-create-model

Subject: A boy getting ready for school, putting on a backpack.

Render style: Comic book; use documentation/references/renders/render_character_v1.png as inspiration.

Lighting: Warm morning light; consult documentation/references/lighting/lighting_character_v1.png.

Setting: A cozy bedroom with school supplies.

Camera: Full-body, three-quarter view at the character's eye level.

Colors: Muted blues with yellow accents.

Output: Editable Blender scene and a 1920x1080 PNG preview.

Inspect the referenced images and choose treatments that fit this brief.
```

## Project Details

### Skills

Explore the available Blender skills for creating, refining, and rendering 3D assets.

- [Browse the skills table](documentation/skills-readme.md)

### References

Explore visual references for camera angles, color palettes, lighting, and rendering styles.

- [Browse the visual reference table](documentation/reference-readme.md)

### Examples

Explore completed Blender examples with editable scenes and rendered previews.

- [Browse the examples table](documentation/examples-readme.md)
- [Review the 2026-10-03 visual refresh](documentation/examples/human-review-2026-10-03.html)

### 📝 Structure

- `skills/`: shared Blender skill sources and the basis for the Claude package.
- `.codex/skills/`: separately curated Codex package with OpenAI metadata, operating guidance, and a Codex-only greybox skill.
- `.claude/skills/`: generated Claude package with a client-specific setup workflow.
- `scripts/`: installation and development validation tools.
- `documentation/references/`: the original camera, colors, lighting and renders directories.
- `documentation/examples/`: example projects and rendered outputs.
- `documentation/`: user guides, visual references, and examples.
- `scripts/script-documentation/`: helper interfaces, source notes, and validation evidence.

To reuse this layout for another theme, follow the [repository adaptation guide](documentation/adapting-repository.md). It identifies the Blender-specific files and checks that must be rewritten before publishing a new catalog.

### 📦 Dependencies

- [Blender](https://www.blender.org/)
- [Official Blender Lab MCP](https://www.blender.org/lab/mcp-server/)
- AI Harness: Ex. [Codex](https://openai.com/codex/), [Claude](https://claude.ai/)

## Contributions

Contributions are welcome! Help improve skills, share examples, fix bugs, or make the documentation clearer—every contribution matters.

- [Read the contribution guide](CONTRIBUTING.md)
- [Report bugs or suggest ideas through Issues](https://github.com/SamuelAsherRivello/ai-skills-blender/issues)
- [Browse or submit Pull Requests](https://github.com/SamuelAsherRivello/ai-skills-blender/pulls)

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
