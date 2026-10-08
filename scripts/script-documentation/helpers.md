# Helper interfaces

Resolve helper paths relative to the installed skill. Python 3.11+ is sufficient for the setup and output helpers; the sprite packer and scene audit run inside Blender. The development validator additionally needs PyYAML.

On Windows, create no auxiliary command windows, including brief flashes. Prefer existing MCP tools. Before executing any example below, establish no-console creation for the outer launcher and its descendants; otherwise report BLOCKED and do not launch. Never open a terminal or retry without suppression. An absolute path or `cmd /c` addresses resolution, not suppression; Blender `--background` and hidden-window styling alone do not prove no flashes.

The setup package includes `scripts/windowless.py`: a bounded captured runner for reviewed console-only commands. Its worker joins a kill-on-close Windows Job before starting the command, so cleanup is scoped to owned descendants. It cannot prevent an arbitrary application from creating its own GUI, and callers must review descendants before use. Output and errors remain available to the caller; avoid printing secrets from raw diagnostics. Preserve the existing Blender editor state.

## Setup

```powershell
python skills/blender-setup/scripts/check_setup.py --format markdown
python skills/blender-setup/scripts/check_setup.py --server blender
```

Exit 0 means all six checks pass. Exit 1 means a failed or blocked check. JSON is the default. Configuration is read from CODEX_HOME/config.toml or ~/.codex/config.toml; no configuration is changed.

The supplemental SDK probe currently reports BLOCKED before launching: the inspected MCP SDK 1.30.0 retries without console-suppression flags and does not guarantee process-tree ownership. No SDK transport is approved yet. Use native session MCP tools for live handshake/scene evidence, and report it separately from helper checks. Do not restart a client or server with unknown launch behavior to bypass this block.

## Render verification

Save a JSON manifest alongside outputs:

```json
{
  "run_id": "preview-001",
  "source": "scene.blend",
  "settings": {"engine": "CYCLES", "samples": 32},
  "outputs": [
    {"path": "frame-001.png", "width": 512, "height": 512, "alpha": true}
  ]
}
```

```powershell
python skills/blender-render/scripts/verify_outputs.py C:\MyOutput\manifest.json
```

Paths resolve relative to the manifest. Every expected frame must be listed. Checks cover source existence, unique output paths, PNG chunk checksums, decompressed scanline structure, dimensions and requested alpha channels. Standard non-interlaced PNGs up to 256 MiB decoded are supported. Alpha-channel presence does not prove transparency coverage. Image inspection is still required for visual quality.

## Sprite packing

Save a manifest beside equal-size RGBA PNG frames:

```json
{
  "width": 128,
  "height": 128,
  "columns": 2,
  "pivot": [0.5, 0.5],
  "frames": [
    {"path": "front.png", "direction": "front", "frame": 0},
    {"path": "right.png", "direction": "right", "frame": 0}
  ]
}
```

Inside the verified Blender MCP execution tool:

```python
import runpy
pack = runpy.run_path("/absolute/installed/skill/scripts/pack_sprites.py")["pack"]
result = pack("/absolute/output/frames.json", "/absolute/output/new-sheet-run")
```

Use native absolute paths for your machine. The output directory must not exist. Outputs are sheet.png and sheet.json. Frame rectangles and normalized pivots use a top-left origin. Input order is preserved; the packer does not trim frames or invent animation timing. Limits are 256 frames and 16 megapixels per sheet. A failed input check leaves prior outputs intact.

## Scene audit

Inside Blender, pass a deliberately scoped collection:

```python
import bpy
import runpy
audit = runpy.run_path("/absolute/installed/skill/scripts/audit_scene.py")["audit"]
result = audit(bpy.data.collections["MyAsset"].objects)
```

Returns version, object dimensions, evaluated vertices/triangles, base vertices, material slots and modifier types. It is read-only and does not provide a GPU memory measurement.

## Maintainer validation

The live acceptance fixture and offline tests are maintained locally under the Git-ignored tests/ directory. They are not included in this distribution. Recorded results and coverage limits are in [acceptance.md](acceptance.md).

Consumers can validate packages with:

```powershell
python -m pip install -r requirements-dev.txt
python scripts/validate-skills.py skills --client codex --require-openai-metadata --require-ten-step-workflow
python scripts/validate-skills.py .codex/skills --client codex --require-openai-metadata --require-ten-step-workflow --link-root .codex/skills
python scripts/validate-skills.py .claude/skills --client claude
python scripts/sync-client-skills.py --check
```

The validator needs PyYAML. On Windows, `python` may resolve to an unusable WindowsApps alias; use `py -3` or the executable path of a verified Python installation instead. Agent-launched checks must still satisfy the repository's no-console process rule. The default validator check is theme-neutral; the optional flags above enforce this Blender catalog's metadata and workflow convention. `--expected-count N` is available when a release deliberately fixes its catalog size. The sync check covers only the generated Claude package; the Codex package is curated separately. See the [adaptation guide](../../documentation/adapting-repository.md) before carrying those optional rules into another theme.
