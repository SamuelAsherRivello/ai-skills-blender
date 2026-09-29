[Back to README.md](../../../../README.md)

# Robot Greeting — review

One creative iteration, delivered for human artistic review on 2026-09-29. Technical corrections and required diagnostic/animation outputs belong to this same build.

## Input and workflow

[Exact prompt](../input/prompt.txt) · [Build source](../input/build.py) · [Visual target](../input/visual-targets/target-01/target.png) · [Target brief/provenance](../input/visual-targets/target-01/brief.md)

Skills used: blender-setup, blender-create-visual-target-2d, blender-materials, blender-light-camera, blender-render, blender-review-optimize, blender-create-model, blender-rig-animate, blender-game-export. Execution used the official Blender Lab MCP in the open editor. Generated targets were comparison references, never substituted for Blender output. Example 06 reused its supplied image.

Source baseline: `421019eccd7e6d518261a8ada79779ac01c41eb6` with local uncommitted gallery and skill changes. This identifies the working baseline, not a claim that all execution sources are committed.

## Output and timing

[Render](result.png) · [Editable Blender scene](result.blend) · [Genuine editor screenshot](editor.png) · [Settings/timings](manifest.json) · [Reopen check](reopen-check.json)

Blender 5.2.2 LTS; Cycles OptiX GPU, 32 samples with denoising, AgX / Medium High Contrast, exposure +0.3; final still 1280×720. Render-call wall time: **7.64 seconds** (soft target <30 seconds; excludes build, bake, export and capture).

Animation/sprite batch: 30.94 seconds total, separate from the still.

## Verification

Greeting_Wave has 24 frames at 12 fps. Inspected beginning, middle, end and positive wave poses; rigid parts remain attached and boots stay grounded. All 24 PNG frames differ. Reimport returned 37 mesh objects, one armature and the named clip (with an import suffix).

Saved file reopened in Blender, with a valid camera, 1280×720 output, relative `//result.png` destination, no linked libraries and no unpacked required image assets. Before this editor capture, both Blender windows were visible and non-minimized. Captured pixels were inspected: the screenshot shows this example's render and real Blender editor panels, not a composited substitute.

[GIF](greeting.gif), [pose sequence](frames/), [animated GLB](robot.glb), [reimport check](export-check.json)

## Target comparison and remaining limits

The target informed the friendly teal/yellow toy proportions. The result has a simpler face and rigid mechanical articulation. The wave mainly twists the forearm, so its silhouette change is subtle. The 24-frame preview lasts about two seconds; GLB key times span 1/12 to 2 seconds (1.9167 seconds between first and last key). The GIF rounds frame durations. No target-engine playback certification is claimed.

No second artistic attempt was made. Technical completion does not imply human approval or photographic equivalence to the target.
