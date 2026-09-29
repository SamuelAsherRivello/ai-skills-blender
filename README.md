# Blender Skills for Codex

Thirteen focused skills for the official Blender Lab MCP connection. Canonical sources live in [skills/](skills/); installed Codex skills go into `.agents/skills` in a project or the user's home.

## Images

### Screenshots

Reference sheets from the optional gallery (inspiration, not generated project output):

<a href="references/render-styles/renders/render_architecture_v1.png"><img src="references/render-styles/renders/render_architecture_v1.png" width="400" alt="Architectural render reference sheet" /></a>
<a href="references/render-styles/renders/render_character_v1.png"><img src="references/render-styles/renders/render_character_v1.png" width="400" alt="Character render reference sheet" /></a>

[Visual references](references/render-styles/README.md) contains 20 user-supplied PNGs organized into camera, colors, lighting and renders, with architectural and character indexes. Textual styles remain usable without the optional gallery.

## Live Demo

These skills run locally in Codex with Blender. There is no hosted demo. See the [live Blender acceptance results](docs/acceptance.md) and [reproducible test instructions](docs/helpers.md#live-acceptance-fixture).

## Table of Contents

1. [Images](#images)
2. [Live Demo](#live-demo)
3. [Getting Started](#getting-started)
4. [Project Details](#project-details)
5. [Credits](#credits)

## Getting Started

Here are the steps.

1. **Install Blender:** [blender.org](https://www.blender.org/download/)
2. **Setup Blender MCP:** [Official setup](https://www.blender.org/lab/mcp-server/)
3. **Install Skills:** Run `./scripts/install-codex.ps1 -Scope User -Skills all` from this repository in PowerShell.
4. **Use Skills:** In Codex, run `$blender-setup`, then request a task such as `$blender-render Render the current scene.`

## Project Details

Windows/Codex is the first support target. Other clients and platforms are not yet verified. Source content remains portable and avoids personal configuration paths.

### 📝 Structure

- skills/: the thirteen independently installable skill folders.
- scripts/: installation and development validation tools.
- references/render-styles/: optional visual references and contribution conventions.
- docs/: input guidance, helper interfaces, source provenance and validation evidence.
- tests/: maintained offline tests and the reproducible Blender acceptance fixture.

Local OpenSpec planning, generated acceptance outputs, environments and caches are excluded from Git. Intentional future PNG references and Blender source assets are not blanket-ignored.

### 📦 AI

Each skill includes `SKILL.md`, Codex metadata in `agents/openai.yaml`, and any required scripts or references. Supporting resources stay with their owning skill so individual installation works.

The optional shared gallery is loaded only when useful. Select a reference by filename and inspect the image before applying its visual characteristics. See [input conventions](docs/inputs.md) and [helper interfaces](docs/helpers.md).

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

### 📦 Packages

- **Blender** supplies the 3D runtime and bundled Python for Blender helpers.
- **Official Blender Lab MCP** connects local Codex to Blender through the separately configured add-on/server.
- **Python 3.11+** runs the standalone setup and output helpers.
- **PyYAML** is the development dependency for skill metadata validation; see [requirements-dev.txt](requirements-dev.txt).
- **PowerShell** runs the Windows installer.

## Credits

### 💡 Contributors

- Samuel Asher Rivello - Over 25 years of game development XP (2026).
- Workflow research and inspiration are recorded in [sources and boundaries](docs/sources.md).
- Reference images were supplied by the repository owner; their original creators and licenses have not been supplied.

### 💡 Contact

- [LinkedIn.com/in/SamuelAsherRivello](https://Linkedin.com/in/SamuelAsherRivello) ⭐
- [GitHub.com/SamuelAsherRivello](https://github.com/SamuelAsherRivello/)
- [Twitter.com/srivello](https://twitter.com/srivello/)
- Resume / Portfolio: [SamuelAsherRivello.com](http://www.SamuelAsherRivello.com)

### 💡 License

A distribution license has not yet been selected for this repository. Reference-image attribution and licensing are recorded as unknown until supplied. No third-party license is implied by inclusion in the gallery.
