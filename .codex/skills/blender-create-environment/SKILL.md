---
name: blender-create-environment
description: Build a coherent Blender environment or modular scene from a setting; use for rooms, landscapes and scene assembly.
---

# blender-create-environment

## Inputs and scope

Accept setting, real-world scale, camera or traversal needs; default to a representative small area first. Honor supplied context, references, output specifications, and technical constraints. State assumptions; ask only when an answer materially changes the work. Textual style needs no reference; inspect an explicitly supplied or known-gallery image before relying on it, and never fetch one automatically.

## Operating boundaries

Read [operating boundaries](../blender-setup/references/operating-boundaries.md) before execution.

## Visual direction

For a new environment with an art-direction brief, prepare one target with `blender-create-visual-target-2d`. Reuse it through nested work, compare genuine previews against the frozen version, and make only in-scope corrections. A supplied reference or prompt-only brief is sufficient when target preparation is unavailable; disclose that limitation.

## Workflow

1. Verify official MCP readiness; interpret setting, style and intended shots. When references are supplied, identify the visible cues that serve the brief (proportions, depth, surface response, context); distinguish quality references from layouts to reproduce and preserve explicit prompt choices.
2. Set units, reference heights and modular dimensions.
3. Plan floor layout, focal points, circulation and visible boundaries.
4. Block out architecture/terrain in a scoped collection, preserving the existing scene.
5. Develop one representative area and inspect its camera view before scaling the scene. Resolve construction depth and contact at the intended viewing distance: openings need recesses, edge thickness, and plausible backing when visible. A pane placed over an opaque wall is not an opening.
6. Build a reusable kit with consistent origins and snapping dimensions.
7. Place or scatter instances with a recorded seed; avoid obstructing required sightlines. Establish a few coherent secondary families instead of copying the hero treatment everywhere. Vary supported dimensions, openings, and condition purposefully; random variation alone does not make context believable.
8. Assign material families and establish broad lighting without hiding layout problems.
9. Inspect camera views, collisions when requested, instance count and render/viewport cost.
10. Save the scene, kit, seeds, views and measured limitations.

## Execution notes


Use instancing for repeated pieces. Check joins and silhouette repetition from the actual camera. Do not imply traversal or collisions were verified unless exercised in the target context.

Treat surrounding geometry as part of the shot and reflective environment. A detailed subject surrounded by flat placeholder masses can still look like a miniature. Budget secondary detail by visible contribution; do not add unrelated props just because a reference contains them. For stylized scenes, keep simplification deliberate and consistent with the subject.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
