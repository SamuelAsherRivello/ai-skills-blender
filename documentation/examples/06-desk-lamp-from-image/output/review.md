[Back to README.md](../../../../README.md)

# Desk Lamp from Image — review

One creative iteration, delivered for human artistic review on 2026-09-29. Technical corrections and required diagnostic/animation outputs belong to this same build.

## Input and workflow

[Exact prompt](../input/prompt.txt) · [Build source](../input/build.py) · [Visual target](../input/visual-targets/target-01/target.png) · [Target brief/provenance](../input/visual-targets/target-01/brief.md)

Skills used: blender-setup, blender-create-visual-target-2d, blender-materials, blender-light-camera, blender-render, blender-review-optimize, blender-convert-2d-3d, blender-create-model. Execution used the official Blender Lab MCP in the open editor. Generated targets were comparison references, never substituted for Blender output. Example 06 reused its supplied image.

Source baseline: `421019eccd7e6d518261a8ada79779ac01c41eb6` with local uncommitted gallery and skill changes. This identifies the working baseline, not a claim that all execution sources are committed.

## Output and timing

[Render](result.png) · [Editable Blender scene](result.blend) · [Genuine editor screenshot](editor.png) · [Settings/timings](manifest.json) · [Reopen check](reopen-check.json)

Blender 5.2.2 LTS; Cycles OptiX GPU, 32 samples with denoising, AgX / Medium High Contrast, exposure +0.3; final still 1280×720. Render-call wall time: **5.93 seconds** (soft target <30 seconds; excludes build, bake, export and capture).

## Verification

Used the top-left Photorealistic panel of the unchanged supplied reference sheet. The model has a hollow shade, articulated arms, base, bulb and cable. Matching, rear and side views demonstrate full 3D geometry.

Saved file reopened in Blender, with a valid camera, 1280×720 output, relative `//result.png` destination, no linked libraries and no unpacked required image assets. Before this editor capture, both Blender windows were visible and non-minimized. Captured pixels were inspected: the screenshot shows this example's render and real Blender editor panels, not a composited substitute.

[Comparison and provenance](comparison.md), [matching view](matching-view.png), [rear view](rear-view.png), [side view](side-view.png)

## Target comparison and remaining limits

The yellow shade, black base and articulated-arm landmarks correspond to the input. Arm angles, shade opening visibility and proportions are approximate. Joint depth, hidden surfaces and real-world dimensions are inferred. This is a plausible reconstruction, not a dimensionally verified duplicate.

No second artistic attempt was made. Technical completion does not imply human approval or photographic equivalence to the target.
