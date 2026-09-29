[Back to README.md](../../../../README.md)

# Fox Sprite Sheet — review

One creative iteration, delivered for human artistic review on 2026-09-29. Technical corrections and required diagnostic/animation outputs belong to this same build.

## Input and workflow

[Exact prompt](../input/prompt.txt) · [Build source](../input/build.py) · [Visual target](../input/visual-targets/target-01/target.png) · [Target brief/provenance](../input/visual-targets/target-01/brief.md)

Skills used: blender-setup, blender-create-visual-target-2d, blender-materials, blender-light-camera, blender-render, blender-review-optimize, blender-create-model, blender-rig-animate, blender-convert-3d-2d. Execution used the official Blender Lab MCP in the open editor. Generated targets were comparison references, never substituted for Blender output. Example 06 reused its supplied image.

Source baseline: `421019eccd7e6d518261a8ada79779ac01c41eb6` with local uncommitted gallery and skill changes. This identifies the working baseline, not a claim that all execution sources are committed.

## Output and timing

[Render](result.png) · [Editable Blender scene](result.blend) · [Genuine editor screenshot](editor.png) · [Settings/timings](manifest.json) · [Reopen check](reopen-check.json)

Blender 5.2.2 LTS; Cycles OptiX GPU, 32 samples with denoising, AgX / Medium High Contrast, exposure +0.3; final still 1280×720. Render-call wall time: **5.13 seconds** (soft target <30 seconds; excludes build, bake, export and capture).

Animation/sprite batch: 8.56 seconds total, separate from the still.

## Verification

Rendered 16 transparent 128x128 frames: rows front/right/back/left and columns frames 1/4/7/10, 250 ms each. Packed sheet is 512x512. Fixed canvas pivot is (64,110); camera scale remains constant. Alpha, ordering, bounds and representative poses inspected. Head/tail motion is intentionally small and legs stay planted.

Saved file reopened in Blender, with a valid camera, 1280×720 output, relative `//result.png` destination, no linked libraries and no unpacked required image assets. Before this editor capture, both Blender windows were visible and non-minimized. Captured pixels were inspected: the screenshot shows this example's render and real Blender editor panels, not a composited substitute.

[Sprite sheet](packed/sheet.png), [packed metadata](packed/sheet.json), [source metadata](sprites.json), [frames](sprites/), [idle GIF](idle.gif)

## Target comparison and remaining limits

The result preserves the target fox colors and large tail but uses simpler angular facial forms. This is rendered low-poly art rather than hand-pixeled art. Front-facing tail movement is subtle at native size; some idle frames repeat. The pivot is a stable canvas anchor, not an automatic foot-contact solve.

No second artistic attempt was made. Technical completion does not imply human approval or photographic equivalence to the target.
