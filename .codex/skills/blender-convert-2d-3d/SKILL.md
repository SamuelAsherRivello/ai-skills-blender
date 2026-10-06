---
name: blender-convert-2d-3d
description: Reconstruct a Blender relief or full model from supplied imagery with explicit depth and hidden-surface assumptions.
---

# blender-convert-2d-3d

## Inputs and scope

Accept image path, intended use, relief/full model and scale; require the actual image before matching. Honor supplied context, references, output specifications, and technical constraints. State assumptions; ask only when an answer materially changes the work. Textual style needs no reference; inspect an explicitly supplied or known-gallery image before relying on it, and never fetch one automatically.

## Operating boundaries

Read [operating boundaries](../blender-setup/references/operating-boundaries.md) before execution.

## Visual direction

For a visually evaluated reconstruction or restyle, prepare one target with `blender-create-visual-target-2d` when the supplied image is not itself the comparison target. Keep it scoped to the request; reuse it across nested work, compare genuine previews only when a target exists, and disclose any unavailable comparison. Do not create a target worker for a purely technical conversion or when the user opts out.

## Workflow

1. Verify readiness and inspect the supplied image, resolution, perspective and occlusion.
2. Choose relief, layered cutout or full 3D reconstruction based on intended use.
3. List observed landmarks and inferred depth/backside geometry.
4. Set reference scale and align a matching camera or image plane.
5. Choose manual/procedural Blender reconstruction without external paid services by default.
6. Block out silhouette and major depth layers.
7. Refine visible forms while keeping inferred details editable.
8. Apply materials or projections without stretching the reference onto unsupported surfaces.
9. Compare the matching view with the source and inspect alternate angles for artifacts.
10. Deliver editable model, comparison views and assumptions; do not promise accurate unseen geometry.

## Execution notes

One image is underdetermined. Ask for extra views only when essential to the user's accuracy target. A depth relief and a complete watertight asset are different deliverables; do not silently substitute one.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
