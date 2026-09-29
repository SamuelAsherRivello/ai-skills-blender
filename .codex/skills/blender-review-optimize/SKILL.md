---
name: blender-review-optimize
description: Audit and optimize Blender asset cost while measuring appearance and downstream behavior.
---

# blender-review-optimize

## Inputs and scope

Accept target collection, budget and permitted changes; default to audit before edits. Also accept optional setting, action/pose, composition, camera, lighting/mood, palette, user references, output specifications and technical constraints when relevant. State assumptions; ask only when a missing answer materially changes the work. A textual style works without reference images. The shared render-style gallery is optional: use an explicitly supplied path or known checkout, inspect a chosen PNG before drawing conclusions, and never fetch missing images automatically.

Use the separately configured official Blender Lab MCP connection. Discover its tools and confirm read-only scene access before mutations; report a connection blocker instead of switching servers. Preserve unrelated objects and settings, scope new content by named collection/run, and checkpoint before destructive edits. Repeated scripts must replace only owned output or create a separate named run. Do not start paid services without authorization.

## Workflow

1. Verify readiness and define scoped assets and optimization goals.
2. Capture baseline views and measured counts using the same camera/settings.
3. Audit evaluated geometry, materials, image sizes, modifiers and animation.
4. Rank findings by measured impact and visible risk.
5. Checkpoint the source before destructive optimization.
6. Apply focused fixes to the owned scope; preserve silhouette and deformation where required.
7. Remeasure using the baseline method.
8. Compare before/after renders at intended display size.
9. Check affected exports, modifiers and animation for regressions.
10. Deliver source, before/after measurements, visual evidence and unresolved findings.

## Execution notes

Use [scripts/audit_scene.py](scripts/audit_scene.py) inside Blender for selected-object counts; pass objects explicitly to audit(). Evaluated geometry can be much larger than base geometry. Texture memory estimates are estimates, not GPU profiler measurements.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
