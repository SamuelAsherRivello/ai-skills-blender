<p>
<img src="https://raw.githubusercontent.com/SamuelAsherRivello/github-repository-template/main/project-name/documentation/samuel-asher-rivello-banner.png" alt="Samuel Asher Rivello" width="600" /><br /><br />
  
<img src="documentation/marketing/images/youtube-thumbnail.png" alt="Blender AI skills YouTube thumbnail" width="600" />
</p>

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-14-orange.svg)](skills/)
[![Blender MCP](https://img.shields.io/badge/Blender_MCP-official-blueviolet.svg)](https://www.blender.org/lab/mcp-server/)
[![Codex](https://img.shields.io/badge/Codex-skills-green.svg)](.codex/INSTALL.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-skills-black.svg)](.claude/INSTALL.md)

# AI Skills Blender

Create, refine, and render 3D assets with fourteen reusable Blender skills.<br />
Shared sources live in [skills/](skills/), with client packages in [.codex/](.codex/INSTALL.md) and [.claude/](.claude/INSTALL.md).

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

### 1. Get the skills

From your project directory, run:

```sh
npx skills@latest add SamuelAsherRivello/ai-skills-blender --copy
```

Choose the Blender skills you want and the agents to install them for, including Codex and Claude Code. Project-local installation is the recommended default. `--copy` installs ordinary files you can edit.

To install globally instead, add `--global`:

```sh
npx skills@latest add SamuelAsherRivello/ai-skills-blender --copy --global
```

### 2. Update the skills

For project-local installations:

```sh
npx skills update --project
```

For global installations:

```sh
npx skills update --global
```

Before using Blender skills, install Blender and configure the official Blender MCP connection. See the [getting started guide](documentation/getting-started-readme.md) for prerequisites and setup. The [Codex](.codex/INSTALL.md) and [Claude Code](.claude/INSTALL.md) package installers remain available as advanced options.

## Use Skills

Claude uses `/skill-name` for the same catalog shown below with Codex `$skill-name` syntax.

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

- `skills/`: shared authoring sources for fourteen skills.
- `.codex/skills/`: generated Codex package with OpenAI metadata.
- `.claude/skills/`: generated Claude package with a client-specific setup workflow.
- `scripts/`: installation and development validation tools.
- `documentation/references/`: the original camera, colors, lighting and renders directories.
- `documentation/examples/`: example projects and rendered outputs.
- `documentation/`: user guides, visual references, and examples.
- `scripts/script-documentation/`: helper interfaces, source notes, and validation evidence.

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
