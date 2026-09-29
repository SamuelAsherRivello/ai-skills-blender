# Blender skills for Codex

Thirteen focused skills for the official Blender Lab MCP connection. Canonical sources live in [skills/](skills/); installed Codex skills go into `.agents/skills` in a project or the user's home.

## Catalog

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

## Prerequisites

Use local Codex on Windows, Blender, and the separately configured **official Blender Lab MCP** add-on/server. Keep versions compatible. The setup helper uses Python 3.11+ and the Python interpreter from the named Codex MCP registration. It does not install or replace servers. Repository validators require `python -m pip install -r requirements-dev.txt`. Blender helpers use Blender's bundled Python; run them through the verified official MCP execution tool or the documented Blender CLI.

## Install

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

## Requests

```text
$blender-create-model A boy getting ready for school, comic-book style.
$blender-render Render the current scene.
$blender-convert-3d-2d Make eight isometric views of the current model as 128x128 transparent sprites.
```

See [input conventions](docs/inputs.md). Subject and style are natural-language inputs, not mandatory flags. Other inputs include deliverable, setting, pose, composition, camera, lighting, palette, supplied references, output specs and technical constraints.

## Repository layout

- skills/: the thirteen independently installable skill folders.
- scripts/: installation and development validation tools.
- references/render-styles/: optional visual references and contribution conventions.
- docs/: input guidance, helper interfaces, source provenance and validation evidence.
- tests/: maintained offline tests and the reproducible Blender acceptance fixture.

Local OpenSpec planning, generated acceptance outputs, environments and caches are excluded from Git. Intentional future PNG references and Blender source assets are not blanket-ignored.

## Reference galleries

[Visual references](references/render-styles/README.md) contains 20 user-supplied PNGs organized into camera, colors, lighting and renders, with architectural and character indexes. Textual styles remain usable without the optional gallery.

## Verify

```powershell
python scripts/validate-skills.py
python skills/blender-setup/scripts/test_check_setup.py
python -m unittest discover -s tests -p "test_*.py"
python skills/blender-setup/scripts/check_setup.py --format markdown
```

See [acceptance results](docs/acceptance.md) for current live exercise evidence and limits. Skills are instructions for Codex, not one-click universal asset generators. Image inspection is part of completion; structural checks alone do not establish artistic quality.

See [helper interfaces](docs/helpers.md) for manifest examples and a reproducible live Blender test command.

Windows/Codex is the first support target. Other clients/platforms, plugin publication and public distribution licensing are deferred. Source content remains portable and avoids personal configuration paths. See [sources and boundaries](docs/sources.md).
