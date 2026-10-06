---
name: blender-light-camera
description: Compose Blender shots and establish lighting, exposure and camera settings; use before final rendering.
---

# blender-light-camera

## Inputs and scope

Accept shot intent, framing, mood, aspect and projection; reuse a suitable existing camera. Honor supplied context, references, output specifications, and technical constraints. State assumptions; ask only when an answer materially changes the work. Textual style needs no reference; inspect an explicitly supplied or known-gallery image before relying on it, and never fetch one automatically.

## Operating boundaries

Read [operating boundaries](../blender-setup/references/operating-boundaries.md) before execution.

## Visual direction

For an art-directed new shot, prepare one target with `blender-create-visual-target-2d` if useful for comparison. Reuse it through nested work, preserve intentional existing composition, and compare only genuine previews. Do not require a target for a technical exposure, framing, or camera repair.

## Workflow

1. Verify readiness and establish subject, mood and output framing.
2. Inspect scene bounds and important surfaces without altering geometry.
3. Select projection, focal length/orthographic scale and camera position deliberately.
4. Set and record color management and exposure baseline. For realistic work, check a neutral surface and dark region before tuning decorative lights; a flat world color or underlit environment can hide material differences even when direct shadows look plausible.
5. Place the key light to reveal shape and direct attention.
6. Add fill/rim/environment light only where it serves the shot.
7. Balance exposure and contrast; check highlights and dark regions.
8. Render a bounded preview using final aspect ratio. Fit the entire required subject or pose with an explicit margin; include raised limbs, handles, and protrusions in camera-space bounds. Account for aspect ratio when choosing orthographic scale or lens distance, and verify the actual image rather than assuming the numerical bounds guarantee framing.
9. Inspect clipping, silhouette, unwanted shadows and depth-of-field focus at output size. Recheck the camera after adding surrounding or reflection geometry: context must not unexpectedly obstruct the subject or flatten its hierarchy.
10. Save named camera/light settings and deliver the reviewed preview.

## Execution notes

Orthographic framing is useful for sprites and diagrams; perspective is a deliberate alternative. Avoid using exposure to conceal an incorrectly scaled light or material. Keep camera clipping planes appropriate to scene scale.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
