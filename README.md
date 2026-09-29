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

Use local Codex on Windows, Blender, and the separately configured **official Blender Lab MCP** add-on/server. Keep versions compatible. The setup helper uses Python 3.11+ and the Python interpreter from the named Codex MCP registration. It does not install or replace servers. Repository validators require `python -m pip install -r requirements-dev.txt`. Blender helpers use Blender's bundled Python; run them through the verified official MCP execution tool or the documented Blender CLI.

### 🛠 Build Project

Skills are Markdown instructions and supporting files; no application build is required. Install the development dependencies and validate the library from the repository root:

```powershell
python -m pip install -r requirements-dev.txt
python scripts/validate-skills.py
```

Install the skills into your chosen Codex scope:

From this repository in PowerShell:

```powershell
# Review a single project installation first
.\scripts\install-codex.ps1 -Scope Project -ProjectPath C:\MyProject -Skills blender-render -DryRun
.\scripts\install-codex.ps1 -Scope Project -ProjectPath C:\MyProject -Skills blender-render

# Install the suite for the current user
.\scripts\install-codex.ps1 -Scope User -Skills all
```

Conflicts stop installation before writes. Explicit `-Replace` preserves backups under `.agents/skill-backups`; review reported paths before restoring. Same-name legacy `~/.codex/skills` entries are warned about and left intact. No live installation is part of authoring this repository. Do not use `-UserRoot` except to deliberately target a different home (tests use temporary homes).

The optional `-GalleryDestination C:\MyReferences\render-styles` copies the reference gallery to that explicit location. Pass its path in future requests. Skills work without it.

### 🛠 Run Project

Open Blender, enable the official MCP add-on and start its bridge. In Codex, check the connection with `$blender-setup`, then request a workflow:

```text
$blender-create-model A boy getting ready for school, comic-book style.
$blender-render Render the current scene.
$blender-convert-3d-2d Make eight isometric views of the current model as 128x128 transparent sprites.
```

See [input conventions](docs/inputs.md). Subject and style are natural-language inputs, not mandatory flags. Other inputs include deliverable, setting, pose, composition, camera, lighting, palette, supplied references, output specs and technical constraints.

Run the repository checks from the root:

```powershell
python scripts/validate-skills.py
python skills/blender-setup/scripts/test_check_setup.py
python -m unittest discover -s tests -p "test_*.py"
python skills/blender-setup/scripts/check_setup.py --format markdown
```

See [acceptance results](docs/acceptance.md) for current live exercise evidence and limits. Skills are instructions for Codex, not one-click universal asset generators. Image inspection is part of completion; structural checks alone do not establish artistic quality.

See [helper interfaces](docs/helpers.md) for manifest examples and a reproducible live Blender test command.

### 🛠 Release Version

Run the validation commands above and review the live acceptance results before sharing updates. The current distribution is direct skill installation from this repository. Automated version releases and plugin publication are not configured yet; public distribution licensing remains to be decided.

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
