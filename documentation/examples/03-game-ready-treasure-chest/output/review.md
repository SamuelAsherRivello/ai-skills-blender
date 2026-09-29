[Back to README.md](../../../../README.md)

# Game-Ready Treasure Chest — review

One creative iteration, delivered for human artistic review on 2026-09-29. Technical corrections and required diagnostic/animation outputs belong to this same build.

## Input and workflow

[Exact prompt](../input/prompt.txt) · [Build source](../input/build.py) · [Visual target](../input/visual-targets/target-01/target.png) · [Target brief/provenance](../input/visual-targets/target-01/brief.md)

Skills used: blender-setup, blender-create-visual-target-2d, blender-materials, blender-light-camera, blender-render, blender-review-optimize, blender-create-model, blender-uv-bake, blender-game-export. Execution used the official Blender Lab MCP in the open editor. Generated targets were comparison references, never substituted for Blender output. Example 06 reused its supplied image.

Source baseline: `421019eccd7e6d518261a8ada79779ac01c41eb6` with local uncommitted gallery and skill changes. This identifies the working baseline, not a claim that all execution sources are committed.

## Output and timing

[Render](result.png) · [Editable Blender scene](result.blend) · [Genuine editor screenshot](editor.png) · [Settings/timings](manifest.json) · [Reopen check](reopen-check.json)

Blender 5.2.2 LTS; Cycles OptiX GPU, 32 samples with denoising, AgX / Medium High Contrast, exposure +0.3; final still 1280×720. Render-call wall time: **5.47 seconds** (soft target <30 seconds; excludes build, bake, export and capture).

Bake calls: 2.18 seconds.

## Verification

Measured 10,990 triangles against the 12,000 budget. Selected-to-active 1024-square base-color and tangent-normal maps are applied and packed. UV/checker, source comparison and normal-map pixels inspected. Reimport returned one mesh with 10,990 triangles.

Saved file reopened in Blender, with a valid camera, 1280×720 output, relative `//result.png` destination, no linked libraries and no unpacked required image assets. Before this editor capture, both Blender windows were visible and non-minimized. Captured pixels were inspected: the screenshot shows this example's render and real Blender editor panels, not a composited substitute.

[GLB](chest.glb), [export check](export-check.json), [UV layout](uv-layout.png), [checker](uv-checker.png), [source comparison](source-comparison.png), [base color](maps/base-color.png), [normal](maps/normal.png)

## Target comparison and remaining limits

The silhouette and wood/metal palette follow the target, but ornament and material richness are simplified. Lid end panels are missing, leaving visible openings; straps have uneven baked highlights. Checker density varies across islands. Uniform roughness and no metallic map reduce material fidelity. These are recorded for human review, not silently accepted as production-ready.

No second artistic attempt was made. Technical completion does not imply human approval or photographic equivalence to the target.
